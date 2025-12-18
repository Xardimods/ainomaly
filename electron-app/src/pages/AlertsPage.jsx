import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Bell, History, Settings, Send, Save, AlertTriangle, CheckCircle, Smartphone, X, Trash2 } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useDialog } from '../context/DialogContext';

const AlertsPage = () => {
    const { t } = useLanguage();
    const { confirm, alert } = useDialog();
    const location = useLocation();
    const [activeTab, setActiveTab] = useState(location.state?.tab || 'config'); // config, rules, history
    const [settings, setSettings] = useState({
        telegram_token: "",
        telegram_chat_id: "",
        telegram_chat_ids: [],
        enabled: false,
        min_duration: 2.0,
        cooldown: 60,
        attach_image: true,
        notification_duration: 5
    });
    const [history, setHistory] = useState([]);
    const [statusMsg, setStatusMsg] = useState("");
    const [testing, setTesting] = useState(false);
    const [scanning, setScanning] = useState(false);
    const [discoveredUsers, setDiscoveredUsers] = useState([]);
    const [newChatId, setNewChatId] = useState("");

    const translateEvent = (eventStr) => {
        if (!eventStr) return "";
        if (eventStr.includes("SIMULACRO") || eventStr.includes("SIMULATION")) return t("events.fall_sim");
        if (eventStr.includes("Caída") || eventStr.includes("Fall")) return t("events.fall");
        if (eventStr.includes("Recuperación") || eventStr.includes("Recovery")) return t("events.recovery");
        if (eventStr.includes("Normal")) return t("events.normal");
        return eventStr;
    };

    const fetchSettings = () => {
        fetch('http://127.0.0.1:8001/alerts/settings')
            .then(res => res.json())
            .then(data => setSettings(data))
            .catch(err => console.error("Error fetching settings:", err));
    };

    const fetchHistory = () => {
        fetch('http://127.0.0.1:8001/alerts/history')
            .then(res => res.json())
            .then(data => setHistory(data))
            .catch(err => console.error("Error fetching history:", err));
    };



    useEffect(() => {
        fetchSettings();
        if (activeTab === 'history') {
            fetchHistory();
        }
    }, [activeTab]);

    const handleSave = () => {
        setStatusMsg(t("alerts.saving"));
        fetch('http://127.0.0.1:8001/alerts/settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(settings)
        })
            .then(res => res.json())
            .then(() => setStatusMsg(t("alerts.saved")))
            .catch(() => setStatusMsg(t("alerts.error")));

        setTimeout(() => setStatusMsg(""), 3000);
    };

    const handleTest = () => {
        setTesting(true);
        setStatusMsg(t("alerts.testing"));

        fetch('http://127.0.0.1:8001/alerts/test', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                telegram_token: settings.telegram_token,
                telegram_chat_id: settings.telegram_chat_id
            })
        })
            .then(res => res.json())
            .then(data => {
                setStatusMsg(data.message);

                // Auto-fill Chat ID if found
                if (data.success && data.chat_id) {
                    const current = settings.telegram_chat_ids || [];
                    if (!current.includes(data.chat_id)) {
                        setSettings(prev => ({ ...prev, telegram_chat_ids: [...current, data.chat_id] }));
                    }
                }

                setTesting(false);
            })
            .catch((e) => {
                console.error(e);
                setStatusMsg(t("alerts.error"));
                setTesting(false);
            });
    };

    const handleScanUsers = () => {
        setScanning(true);
        setStatusMsg(t("alerts.scanning"));
        fetch('http://127.0.0.1:8001/alerts/discover', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ telegram_token: settings.telegram_token })
        })
            .then(res => res.json())
            .then(data => {
                setDiscoveredUsers(data);
                setStatusMsg(data.length > 0 ? `${t("alerts.found")} ${data.length}` : t("alerts.no_users"));
                setScanning(false);
            })
            .catch(() => {
                setStatusMsg(t("alerts.error"));
                setScanning(false);
            });
    };

    const handleFullTest = async () => {
        const confirmed = await confirm(t("alerts.sim_confirm"), {
            title: t("alerts.data.simulate") || "Simular Alerta",
            confirmText: t("alerts.simulate") || "Simular",
            variant: "warning"
        });
        if (!confirmed) return;

        setStatusMsg(t("alerts.sending"));
        fetch('http://127.0.0.1:8001/alerts/test_full', { method: 'POST' })
            .then(res => res.json())
            .then(() => setStatusMsg(t("alerts.sent")))
            .catch(() => setStatusMsg(t("alerts.error")));
    };

    const handleDeleteAlert = async (id) => {
        const confirmed = await confirm(t("alerts.history_delete_confirm"), {
            variant: 'danger',
            confirmText: 'Eliminar'
        });
        if (!confirmed) return;

        fetch(`http://127.0.0.1:8001/alerts/history/${id}`, { method: 'DELETE' })
            .then(async res => {
                if (res.ok) {
                    setHistory(prev => prev.filter(item => item.id !== id));
                } else {
                    await alert(t("alerts.error"), { variant: 'danger' });
                }
            })
            .catch(err => console.error(err));
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-500 max-w-6xl mx-auto">
            <header className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-2 tracking-tight transition-colors">{t("alerts.title")}</h2>
                    <p className="text-slate-500 dark:text-slate-400 transition-colors">{t("alerts.subtitle")}</p>
                </div>
                {statusMsg && (
                    <div className="bg-blue-600/20 text-blue-600 dark:text-blue-400 px-4 py-2 rounded-lg text-sm font-medium border border-blue-500/30 animate-in slide-in-from-top-2">
                        {statusMsg}
                    </div>
                )}
            </header>

            {/* Tabs */}
            <div className="flex gap-4 border-b border-slate-200 dark:border-white/5 pb-1 transition-colors">
                <button
                    onClick={() => setActiveTab('config')}
                    className={`pb-3 px-4 text-sm font-medium transition-colors relative ${activeTab === 'config' ? 'text-blue-600 dark:text-blue-400' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'}`}
                >
                    <div className="flex items-center gap-2">
                        <Smartphone size={18} /> {t("alerts.tabs.config")}
                    </div>
                    {activeTab === 'config' && <div className="absolute bottom-0 left-0 w-full h-0.5 bg-blue-500 rounded-t-full"></div>}
                </button>
                <button
                    onClick={() => setActiveTab('rules')}
                    className={`pb-3 px-4 text-sm font-medium transition-colors relative ${activeTab === 'rules' ? 'text-blue-600 dark:text-blue-400' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'}`}
                >
                    <div className="flex items-center gap-2">
                        <Settings size={18} /> {t("alerts.tabs.rules")}
                    </div>
                    {activeTab === 'rules' && <div className="absolute bottom-0 left-0 w-full h-0.5 bg-blue-500 rounded-t-full"></div>}
                </button>
                <button
                    onClick={() => setActiveTab('history')}
                    className={`pb-3 px-4 text-sm font-medium transition-colors relative ${activeTab === 'history' ? 'text-blue-600 dark:text-blue-400' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'}`}
                >
                    <div className="flex items-center gap-2">
                        <History size={18} /> {t("alerts.tabs.history")}
                    </div>
                    {activeTab === 'history' && <div className="absolute bottom-0 left-0 w-full h-0.5 bg-blue-500 rounded-t-full"></div>}
                </button>
            </div>

            {/* Content */}
            <div className="bg-white dark:bg-white/5 p-6 rounded-2xl border border-slate-200 dark:border-white/5 shadow-sm dark:shadow-none transition-colors">
                {activeTab === 'config' && (
                    <div className="space-y-6 max-w-3xl">
                        <div className="grid gap-6">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2 transition-colors">Telegram Bot Token</label>
                                <input
                                    type="text"
                                    className="w-full bg-slate-50 dark:bg-black/20 border border-slate-200 dark:border-white/10 rounded-lg px-4 py-3 text-slate-900 dark:text-white focus:outline-none focus:border-blue-500 transition-colors font-mono text-sm"
                                    placeholder="123456789:ABCdefGHIjklMNOpqrsTUVwxYZ"
                                    value={settings.telegram_token}
                                    onChange={e => setSettings({ ...settings, telegram_token: e.target.value })}
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2 transition-colors">{t("alerts.config.chat_ids")}</label>

                                <div className="flex flex-wrap gap-2 mb-3 min-h-[32px] content-center">
                                    {(settings.telegram_chat_ids || []).map((id, idx) => (
                                        <div key={idx} className="bg-blue-500/10 border border-blue-500/30 text-blue-600 dark:text-blue-200 pl-3 pr-2 py-1 rounded-full text-xs font-medium flex items-center gap-2 animate-in zoom-in-50 duration-200">
                                            <span>{id}</span>
                                            <button
                                                onClick={() => {
                                                    const newIds = settings.telegram_chat_ids.filter(x => x !== id);
                                                    setSettings({ ...settings, telegram_chat_ids: newIds });
                                                }}
                                                className="hover:text-rose-500 dark:hover:text-white p-0.5 rounded-full hover:bg-rose-500/10 dark:hover:bg-white/10 transition-colors"
                                            >
                                                <X size={14} />
                                            </button>
                                        </div>
                                    ))}
                                    {(settings.telegram_chat_ids || []).length === 0 && (
                                        <span className="text-slate-400 text-sm italic py-1">{t("alerts.config.no_ids")}</span>
                                    )}
                                </div>

                                <div className="flex gap-2 mb-2">
                                    <input
                                        type="text"
                                        className="flex-1 bg-slate-50 dark:bg-black/20 border border-slate-200 dark:border-white/10 rounded-lg px-4 py-3 text-slate-900 dark:text-white focus:outline-none focus:border-blue-500 transition-colors font-mono text-sm placeholder:text-slate-400 dark:placeholder:text-slate-600"
                                        placeholder={t("alerts.config.add_id_placeholder")}
                                        value={newChatId}
                                        onChange={e => setNewChatId(e.target.value)}
                                        onKeyDown={e => {
                                            if (e.key === 'Enter' && newChatId) {
                                                const current = settings.telegram_chat_ids || [];
                                                if (!current.includes(newChatId)) {
                                                    setSettings({ ...settings, telegram_chat_ids: [...current, newChatId] });
                                                    setNewChatId("");
                                                }
                                            }
                                        }}
                                    />
                                    <button
                                        onClick={() => {
                                            if (newChatId) {
                                                const current = settings.telegram_chat_ids || [];
                                                if (!current.includes(newChatId)) {
                                                    setSettings({ ...settings, telegram_chat_ids: [...current, newChatId] });
                                                    setNewChatId("");
                                                }
                                            }
                                        }}
                                        className="px-4 bg-slate-100 hover:bg-slate-200 dark:bg-white/10 dark:hover:bg-white/20 rounded-lg text-slate-700 dark:text-white border border-slate-200 dark:border-white/10 transition-colors"
                                    >
                                        <CheckCircle size={18} />
                                    </button>
                                </div>

                                <div className="mt-2">
                                    <button
                                        onClick={handleScanUsers}
                                        disabled={scanning || !settings.telegram_token}
                                        className="text-xs text-blue-600 dark:text-blue-400 hover:text-blue-500 dark:hover:text-blue-300 font-medium flex items-center gap-1 mb-2 transition-colors"
                                    >
                                        {scanning ? "Buscando..." : `🔍 ${t("alerts.config.scan_recent")}`}
                                    </button>

                                    {discoveredUsers.length > 0 && (
                                        <div className="bg-slate-50 dark:bg-slate-900/50 rounded-lg p-2 border border-slate-200 dark:border-white/5 space-y-1 max-h-40 overflow-y-auto animate-in fade-in slide-in-from-top-2">
                                            {discoveredUsers.map(u => {
                                                const isAdded = (settings.telegram_chat_ids || []).includes(u.id);
                                                return (
                                                    <button
                                                        key={u.id}
                                                        onClick={() => {
                                                            const current = settings.telegram_chat_ids || [];
                                                            if (current.includes(u.id)) {
                                                                setSettings({ ...settings, telegram_chat_ids: current.filter(x => x !== u.id) });
                                                            } else {
                                                                setSettings({ ...settings, telegram_chat_ids: [...current, u.id] });
                                                            }
                                                        }}
                                                        className={`w-full text-left p-2 hover:bg-slate-100 dark:hover:bg-white/5 rounded-md flex justify-between items-center group transition-colors ${isAdded ? 'bg-blue-500/10' : ''}`}
                                                    >
                                                        <div>
                                                            <p className={`text-sm font-medium ${isAdded ? 'text-blue-600 dark:text-blue-200' : 'text-slate-700 dark:text-slate-200'}`}>{u.name}</p>
                                                            <p className="text-xs text-slate-500 uppercase tracking-wider text-[10px]">{u.type} • {u.id}</p>
                                                        </div>
                                                        {isAdded ? <CheckCircle size={16} className="text-emerald-500" /> : <span className="text-slate-600 text-xs group-hover:text-blue-500 dark:group-hover:text-blue-400 opacity-0 group-hover:opacity-100 transition-opacity">Agregar</span>}
                                                    </button>
                                                );
                                            })}
                                        </div>
                                    )}
                                </div>
                                <p className="text-xs text-slate-500 mt-1">{t("alerts.config.multiple_ids_hint")}</p>
                            </div>

                            <div className="flex items-center gap-3 p-4 bg-slate-50 dark:bg-white/5 rounded-xl border border-slate-200 dark:border-white/5 transition-colors">
                                <button
                                    onClick={() => setSettings({ ...settings, enabled: !settings.enabled })}
                                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${settings.enabled ? 'bg-blue-600' : 'bg-slate-300 dark:bg-slate-700'}`}
                                >
                                    <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${settings.enabled ? 'translate-x-6' : 'translate-x-1'}`} />
                                </button>
                                <span className="text-sm font-medium text-slate-900 dark:text-white transition-colors">{t("alerts.config.enable_global")}</span>
                            </div>

                            <div>
                                <div className="flex justify-between mb-2">
                                    <label className="text-sm font-medium text-slate-700 dark:text-slate-300 transition-colors">{t("alerts.config.notif_duration")}</label>
                                    <span className="text-blue-600 dark:text-blue-400 font-mono bg-blue-100 dark:bg-blue-900/20 px-2 rounded">{settings.notification_duration || 5}s</span>
                                </div>
                                <input
                                    type="range"
                                    min="3" max="20" step="1"
                                    value={settings.notification_duration || 5}
                                    onChange={e => setSettings({ ...settings, notification_duration: parseInt(e.target.value) })}
                                    className="w-full accent-blue-500 h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer"
                                />
                                <p className="text-xs text-slate-500 mt-2">{t("alerts.config.notif_duration_hint")}</p>
                            </div>
                        </div>

                        <div className="flex gap-4 pt-4 border-t border-slate-200 dark:border-white/5">
                            <button
                                onClick={handleSave}
                                className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium transition-all shadow-lg shadow-blue-900/20 active:scale-95"
                            >
                                <Save size={18} /> {t("alerts.save")}
                            </button>
                            <button
                                onClick={handleTest}
                                disabled={testing}
                                className="flex items-center gap-2 px-6 py-2.5 bg-slate-100 hover:bg-slate-200 dark:bg-white/5 dark:hover:bg-white/10 text-slate-700 dark:text-white rounded-lg font-medium transition-all border border-slate-200 dark:border-white/10"
                            >
                                <Send size={18} /> {testing ? t("alerts.testing") : t("alerts.test")}
                            </button>
                        </div>
                    </div>
                )}

                {activeTab === 'rules' && (
                    <div className="space-y-8 max-w-3xl">
                        <section>
                            <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2 transition-colors">
                                <AlertTriangle size={20} className="text-amber-500 dark:text-amber-400" />
                                {t("alerts.rules.fall_detection")}
                            </h3>
                            <div className="space-y-6 pl-2">
                                <div>
                                    <div className="flex justify-between mb-2">
                                        <label className="text-sm font-medium text-slate-700 dark:text-slate-300 transition-colors">{t("alerts.rules.min_duration")}</label>
                                        <span className="text-blue-600 dark:text-blue-400 font-mono bg-blue-100 dark:bg-blue-900/20 px-2 rounded">{settings.min_duration}s</span>
                                    </div>
                                    <input
                                        type="range"
                                        min="0.5" max="10" step="0.5"
                                        value={settings.min_duration}
                                        onChange={e => setSettings({ ...settings, min_duration: parseFloat(e.target.value) })}
                                        className="w-full accent-blue-500 h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer"
                                    />
                                    <p className="text-xs text-slate-500 mt-2">{t("alerts.rules.min_duration_hint")}</p>
                                </div>

                                <div>
                                    <div className="flex justify-between mb-2">
                                        <label className="text-sm font-medium text-slate-700 dark:text-slate-300 transition-colors">{t("alerts.rules.cooldown")}</label>
                                        <span className="text-blue-600 dark:text-blue-400 font-mono bg-blue-100 dark:bg-blue-900/20 px-2 rounded">{settings.cooldown}s</span>
                                    </div>
                                    <input
                                        type="range"
                                        min="10" max="300" step="10"
                                        value={settings.cooldown}
                                        onChange={e => setSettings({ ...settings, cooldown: parseInt(e.target.value) })}
                                        className="w-full accent-blue-500 h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer"
                                    />
                                    <p className="text-xs text-slate-500 mt-2">{t("alerts.rules.cooldown_hint")}</p>
                                </div>
                            </div>
                        </section>

                        <section className="border-t border-slate-200 dark:border-white/5 pt-6 transition-colors">
                            <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2 transition-colors">
                                <CheckCircle size={20} className="text-emerald-500 dark:text-emerald-400" />
                                {t("alerts.rules.content")}
                            </h3>
                            <div className="space-y-3">
                                <label className="flex items-center gap-3 p-3 bg-slate-50 dark:bg-white/5 rounded-lg cursor-pointer hover:bg-slate-100 dark:hover:bg-white/10 transition">
                                    <input
                                        type="checkbox"
                                        checked={settings.attach_image}
                                        onChange={e => setSettings({ ...settings, attach_image: e.target.checked })}
                                        className="w-5 h-5 rounded border-slate-300 dark:border-slate-600 text-blue-600 focus:ring-blue-500 bg-white dark:bg-slate-700"
                                    />
                                    <span className="text-slate-700 dark:text-slate-200 transition-colors">{t("alerts.rules.attach_images")}</span>
                                </label>
                            </div>
                        </section>

                        <div className="flex gap-4 pt-6 border-t border-slate-200 dark:border-white/5 transition-colors">
                            <button
                                onClick={handleSave}
                                className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium transition-all shadow-lg shadow-blue-900/20"
                            >
                                <Save size={18} /> {t("alerts.save_rules")}
                            </button>
                            <button
                                onClick={handleFullTest}
                                className="flex items-center gap-2 px-6 py-2.5 bg-rose-500/10 hover:bg-rose-500/20 text-rose-600 dark:text-rose-400 rounded-lg font-medium transition-all border border-rose-500/20 ml-auto"
                            >
                                <Bell size={18} /> {t("alerts.simulate")}
                            </button>
                        </div>
                    </div>
                )}

                {activeTab === 'history' && (
                    <div className="space-y-4">
                        <div className="flex justify-between items-center mb-4">
                            <p className="text-slate-500 dark:text-slate-400 text-sm">{t("alerts.history.showing_latest")}</p>
                            <button onClick={fetchHistory} className="text-blue-600 dark:text-blue-400 hover:text-blue-500 dark:hover:text-blue-300 text-sm font-medium transition-colors">{t("alerts.history.refresh")}</button>
                        </div>
                        <div className="rounded-xl overflow-hidden border border-slate-200 dark:border-white/5">
                            <table className="w-full text-left">
                                <thead className="bg-slate-50 dark:bg-white/5 text-slate-500 dark:text-slate-400 text-xs uppercase tracking-wider transition-colors">
                                    <tr>
                                        <th className="p-4">{t("alerts.table.date")}</th>
                                        <th className="p-4">{t("alerts.table.camera")}</th>
                                        <th className="p-4">{t("alerts.table.event")}</th>
                                        <th className="p-4">{t("alerts.table.status")}</th>
                                        <th className="p-4 text-right">{t("alerts.table.details")}</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-200 dark:divide-white/5 transition-colors">
                                    {history.length > 0 ? (
                                        history.map((alert, idx) => (
                                            <tr key={alert.id || idx} className="hover:bg-slate-50 dark:hover:bg-white/5 transition-colors group">
                                                <td className="p-4 text-slate-700 dark:text-slate-300 font-mono text-sm">{alert.date}</td>
                                                <td className="p-4 text-slate-900 dark:text-white font-medium">{alert.camera}</td>
                                                <td className="p-4">
                                                    <span className="px-2 py-1 rounded-md bg-rose-500/10 text-rose-600 dark:text-rose-400 text-xs font-bold border border-rose-500/20">
                                                        {translateEvent(alert.event)}
                                                    </span>
                                                </td>
                                                <td className="p-4">
                                                    {alert.status === "Enviado" ? (
                                                        <span className="text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5 text-sm">
                                                            <CheckCircle size={14} /> Enviado
                                                        </span>
                                                    ) : (
                                                        <span className="text-slate-500 text-sm">{alert.status}</span>
                                                    )}
                                                </td>
                                                <td className="p-4 text-right">
                                                    <div className="flex items-center justify-end gap-3">
                                                        <span className="text-slate-500 text-xs max-w-xs truncate">{alert.details}</span>
                                                        <button
                                                            onClick={() => handleDeleteAlert(alert.id)}
                                                            className="text-slate-400 hover:text-rose-500 opacity-0 group-hover:opacity-100 transition-all p-1.5 hover:bg-rose-500/10 rounded-lg"
                                                            title="Eliminar del historial"
                                                            disabled={!alert.id}
                                                        >
                                                            <Trash2 size={16} />
                                                        </button>
                                                    </div>
                                                </td>
                                            </tr>
                                        ))
                                    ) : (
                                        <tr>
                                            <td colSpan={5} className="p-8 text-center text-slate-500">
                                                {t("alerts.history.empty")}
                                            </td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default AlertsPage;
