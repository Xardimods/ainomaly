import React from 'react';
import { Save } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useLanguage } from '../context/LanguageContext';
import { useDialog } from '../context/DialogContext';

const Settings = () => {
    const { theme, toggleTheme } = useTheme();
    const { language, setLanguage, t } = useLanguage();
    const { alert } = useDialog();

    const [settings, setSettings] = React.useState({
        deviceName: "",
        sensitivity: 50,
        autoSave: true,
        telegramNotify: false
    });
    const [loading, setLoading] = React.useState(true);

    React.useEffect(() => {
        fetch('http://127.0.0.1:8001/settings')
            .then(res => res.json())
            .then(data => {
                setSettings(data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to load settings", err);
                setLoading(false);
            });
    }, []);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setSettings(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleSave = () => {
        // Save Settings to Backend
        fetch('http://127.0.0.1:8001/settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(settings)
        })
            .then(res => res.json())
            .then(async () => await alert(t("settings.save") + " OK", { variant: 'success' }))
            .catch(async () => await alert("Error Saving Settings", { variant: 'danger' }));
    };

    if (loading) return <div className="text-slate-900 dark:text-white">Loading...</div>;

    return (
        <div className="space-y-6 max-w-4xl animate-in fade-in duration-500">
            <header>
                <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-2 tracking-tight transition-colors">{t("settings.title")}</h2>
                <p className="text-slate-500 dark:text-slate-400 transition-colors">{t("settings.subtitle")}</p>
            </header>

            <section className="bg-white dark:bg-white/5 shadow-sm dark:shadow-none rounded-2xl p-8 space-y-8 border border-slate-200 dark:border-white/5 transition-all">
                <div>
                    <h3 className="text-lg font-semibold mb-6 text-slate-900 dark:text-white flex items-center gap-2 transition-colors">
                        <span className="w-1 h-6 bg-blue-500 rounded-full shadow-[0_0_10px_#3b82f6]"></span>
                        {t("settings.general")}
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-700 dark:text-slate-300 transition-colors">{t("settings.device_name")}</label>
                            <input
                                type="text"
                                name="deviceName"
                                value={settings.deviceName}
                                onChange={handleChange}
                                className="w-full bg-slate-100 dark:bg-black/20 border border-slate-200 dark:border-white/10 rounded-xl px-4 py-3 outline-none focus:border-blue-500 focus:bg-blue-500/5 text-slate-900 dark:text-slate-200 transition-all placeholder:text-slate-400 dark:placeholder:text-slate-600"
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-700 dark:text-slate-300 transition-colors">{t("settings.language")}</label>
                            <select
                                name="language"
                                value={language}
                                onChange={(e) => setLanguage(e.target.value)}
                                className="w-full bg-slate-100 dark:bg-black/20 border border-slate-200 dark:border-white/10 rounded-xl px-4 py-3 outline-none focus:border-blue-500 focus:bg-blue-500/5 text-slate-900 dark:text-slate-200 transition-all appearance-none cursor-pointer"
                            >
                                <option className="bg-white dark:bg-slate-900" value="es">Español</option>
                                <option className="bg-white dark:bg-slate-900" value="en">English</option>
                            </select>
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-700 dark:text-slate-300 transition-colors">{t("settings.theme")}</label>
                            <button
                                onClick={toggleTheme}
                                className="w-full flex items-center justify-between bg-slate-100 dark:bg-black/20 border border-slate-200 dark:border-white/10 rounded-xl px-4 py-3 text-slate-900 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-white/5 transition-all"
                            >
                                <span>{theme === 'dark' ? 'Modo Oscuro' : 'Modo Claro'}</span>
                                <div className={`w-10 h-6 rounded-full p-1 transition-colors ${theme === 'dark' ? 'bg-blue-600' : 'bg-slate-400'}`}>
                                    <div className={`w-4 h-4 bg-white rounded-full transition-transform ${theme === 'dark' ? 'translate-x-4' : ''}`}></div>
                                </div>
                            </button>
                        </div>
                    </div>
                </div>

                <hr className="border-slate-200 dark:border-white/5 transition-colors" />

                <div>
                    <h3 className="text-lg font-semibold mb-6 text-slate-900 dark:text-white flex items-center gap-2 transition-colors">
                        <span className="w-1 h-6 bg-emerald-500 rounded-full shadow-[0_0_10px_#10b981]"></span>
                        {t("settings.ai_detection")}
                    </h3>
                    <div className="space-y-4">
                        <div className="flex items-center justify-between p-4 bg-slate-50 dark:bg-white/5 rounded-xl border border-slate-200 dark:border-white/5 hover:bg-slate-100 dark:hover:bg-white/10 transition-colors group cursor-pointer">
                            <span className="text-slate-700 dark:text-slate-300 font-medium transition-colors">{t("settings.sensitivity")}: {settings.sensitivity}%</span>
                            <input
                                type="range"
                                name="sensitivity"
                                min="0" max="100"
                                value={settings.sensitivity}
                                onChange={handleChange}
                                className="w-48 accent-blue-500 cursor-pointer"
                            />
                        </div>
                        <div className="flex items-center justify-between p-4 bg-slate-50 dark:bg-white/5 rounded-xl border border-slate-200 dark:border-white/5 hover:bg-slate-100 dark:hover:bg-white/10 transition-colors group cursor-pointer">
                            <span className="text-slate-700 dark:text-slate-300 font-medium group-hover:text-slate-900 dark:group-hover:text-white transition-colors">{t("settings.autosave")}</span>
                            <label className="relative inline-flex items-center cursor-pointer">
                                <input
                                    type="checkbox"
                                    name="autoSave"
                                    checked={settings.autoSave}
                                    onChange={handleChange}
                                    className="sr-only peer"
                                />
                                <div className="w-11 h-6 bg-slate-300 dark:bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                            </label>
                        </div>
                        <div className="flex items-center justify-between p-4 bg-slate-50 dark:bg-white/5 rounded-xl border border-slate-200 dark:border-white/5 hover:bg-slate-100 dark:hover:bg-white/10 transition-colors group cursor-pointer">
                            <span className="text-slate-700 dark:text-slate-300 font-medium group-hover:text-slate-900 dark:group-hover:text-white transition-colors">{t("settings.telegram_notify")}</span>
                            <label className="relative inline-flex items-center cursor-pointer">
                                <input
                                    type="checkbox"
                                    name="telegramNotify"
                                    checked={settings.telegramNotify}
                                    onChange={handleChange}
                                    className="sr-only peer"
                                />
                                <div className="w-11 h-6 bg-slate-300 dark:bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                            </label>
                        </div>
                    </div>
                </div>

                <div className="flex justify-end pt-4">
                    <button
                        onClick={handleSave}
                        className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white px-8 py-3 rounded-xl font-medium transition-all shadow-lg shadow-blue-900/40 flex items-center gap-2 hover:-translate-y-0.5"
                    >
                        <Save size={18} />
                        {t("settings.save")}
                    </button>
                </div>
            </section>
        </div>
    );
};

export default Settings;
