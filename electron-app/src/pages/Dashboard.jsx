import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Activity, ShieldCheck, HardDrive, Wifi, Video, AlertTriangle, X } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

const StatCard = ({ title, value, icon: Icon, color, trend }) => ( // eslint-disable-line no-unused-vars
    <div className="bg-white dark:bg-white/5 border border-slate-200 dark:border-white/5 shadow-sm dark:shadow-none p-6 rounded-2xl relative overflow-hidden group hover:-translate-y-1 transition-all duration-300">
        <div className={`absolute -right-6 -top-6 w-24 h-24 rounded-full opacity-10 blur-xl ${color}`}></div>

        <div className="flex justify-between items-start mb-4 relative z-10">
            <div className={`p-3 rounded-xl bg-slate-100 dark:bg-white/5 border border-slate-200 dark:border-white/10 ${color.replace('bg-', 'text-')}`}>
                <Icon size={24} />
            </div>
            {trend && (
                <span className={`text-xs px-2 py-1 rounded-full border ${trend > 0
                    ? 'border-emerald-500/20 text-emerald-600 dark:text-emerald-400 bg-emerald-500/10'
                    : 'border-rose-500/20 text-rose-600 dark:text-rose-400 bg-rose-500/10'
                    }`}>
                    {trend > 0 ? '+' : ''}{trend}%
                </span>
            )}
        </div>

        <div className="relative z-10">
            <h3 className="text-slate-500 dark:text-slate-400 text-sm font-medium mb-1">{title}</h3>
            <p className="text-3xl font-bold text-slate-900 dark:text-white tracking-tight">{value}</p>
        </div>
    </div>
);

const Dashboard = () => {
    const { t } = useLanguage();
    const [status, setStatus] = useState({
        connected: false,
        camera_status: 'Checking...',
        system: { cpu: 0, ram: 0 },
        storage: { percent: 0, free_gb: 0 }
    });
    const [date, setDate] = useState(new Date());
    const [alertsCount, setAlertsCount] = useState(0);
    const [recentAlerts, setRecentAlerts] = useState([]);
    const [selectedAlert, setSelectedAlert] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const timer = setInterval(() => setDate(new Date()), 60000);
        return () => clearInterval(timer);
    }, []);

    useEffect(() => {
        const interval = setInterval(() => {
            fetch('http://127.0.0.1:8001/status')
                .then(res => res.json())
                .then(data => setStatus(data))
                .catch(() => setStatus(prev => ({ ...prev, connected: false, camera_status: 'Offline' })));

            fetch('http://127.0.0.1:8001/alerts/history')
                .then(res => res.json())
                .then(data => {
                    setAlertsCount(data.length);
                    setRecentAlerts(data.slice(0, 5));
                })
                .catch(e => console.error(e));

        }, 2000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="space-y-8 animate-in fade-in duration-500 max-w-7xl mx-auto">
            {/* Header */}
            <header className="flex justify-between items-end">
                <div>
                    <h2 className="text-4xl font-bold text-slate-900 dark:text-white mb-2 tracking-tight transition-colors">{t("dash.title")}</h2>
                    <p className="text-slate-500 dark:text-slate-400 transition-colors">{t("dash.subtitle")}</p>
                </div>
                <div className="text-right bg-white dark:bg-white/5 px-4 py-2 rounded-xl border border-slate-200 dark:border-white/5 shadow-sm dark:shadow-none transition-colors">
                    <p className="text-sm font-medium text-slate-700 dark:text-slate-300">
                        {date.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long' })}
                    </p>
                    <p className="text-xs text-slate-500 uppercase tracking-widest font-mono">
                        {date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}
                    </p>
                </div>
            </header>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title={t("dash.system_status")}
                    value={status.connected ? "Online" : "Offline"}
                    icon={Wifi}
                    color={status.connected ? "bg-emerald-500" : "bg-rose-500"}
                />
                <StatCard
                    title={t("dash.cameras_active")}
                    value={status.camera_status}
                    icon={Activity}
                    color="bg-blue-500"
                />
                <StatCard
                    title={t("dash.recent_alerts")}
                    value={alertsCount.toString()}
                    icon={ShieldCheck}
                    color="bg-amber-500"
                    trend={alertsCount > 0 ? 10 : 0}
                />
                <StatCard
                    title={t("dash.storage")}
                    value={`${status.storage?.percent || 0}%`}
                    icon={HardDrive}
                    color={(status.storage?.percent || 0) > 90 ? "bg-rose-500" : "bg-purple-500"}
                    trend={0}
                />
            </div>

            {/* Bento Grid layout for bottom section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Recent Activity */}
                <div className="lg:col-span-2 bg-white dark:bg-white/5 p-6 rounded-2xl border border-slate-200 dark:border-white/5 shadow-sm dark:shadow-none transition-all">
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="text-xl font-bold text-slate-900 dark:text-white transition-colors">{t("dash.recent_alerts")}</h3>
                        <button
                            onClick={() => navigate('/alerts', { state: { tab: 'history' } })}
                            className="text-xs text-blue-600 dark:text-blue-400 hover:text-blue-500 dark:hover:text-blue-300 transition-colors"
                        >
                            {t("dash.view_all")}
                        </button>
                    </div>

                    <div className="space-y-4">
                        {recentAlerts.length > 0 ? (
                            recentAlerts.map((alert, idx) => (
                                <div
                                    key={idx}
                                    onClick={() => setSelectedAlert(alert)}
                                    className="group flex items-center justify-between p-4 rounded-xl bg-slate-50 dark:bg-white/5 hover:bg-slate-100 dark:hover:bg-white/10 border border-slate-200 dark:border-white/5 transition-all cursor-pointer"
                                >
                                    <div className="flex items-center gap-4">
                                        <div className={`w-12 h-12 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform ${alert.event.includes("Caída") ? "bg-rose-500/20 text-rose-600 dark:text-rose-400" : "bg-indigo-500/20 text-indigo-600 dark:text-indigo-400"
                                            }`}>
                                            {alert.event.includes("Caída") ? <AlertTriangle size={20} /> : <Video size={20} />}
                                        </div>
                                        <div>
                                            <p className="text-slate-900 dark:text-white font-medium">{alert.event}</p>
                                            <p className="text-xs text-slate-500 dark:text-slate-400">{alert.camera} • {alert.date}</p>
                                        </div>
                                    </div>
                                    <span className={`text-xs px-3 py-1 rounded-lg transition-colors ${alert.status === "Enviado"
                                        ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20"
                                        : "bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-500"
                                        }`}>
                                        {alert.status}
                                    </span>
                                </div>
                            ))
                        ) : (
                            <div className="text-center py-8 text-slate-500 text-sm">
                                <p>{t("dash.no_alerts")}</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Server Status */}
                <div className="bg-white dark:bg-white/5 p-6 rounded-2xl border border-slate-200 dark:border-white/5 shadow-sm dark:shadow-none flex flex-col transition-all">
                    <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-6 transition-colors">{t("dash.system_status")}</h3>

                    <div className="space-y-6 flex-1">
                        <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                                <span className="text-slate-500 dark:text-slate-400 transition-colors">{t("dash.cpu_usage")}</span>
                                <span className={status.connected ? "text-emerald-600 dark:text-emerald-400" : "text-rose-600 dark:text-rose-400"} >
                                    {status.system?.cpu || 0}%
                                </span>
                            </div>
                            <div className="w-full h-2 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden transition-colors">
                                <div
                                    className={`h-full rounded-full bg-emerald-500 transition-all duration-1000`}
                                    style={{ width: `${status.system?.cpu || 0}%` }}
                                ></div>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                                <span className="text-slate-500 dark:text-slate-400 transition-colors">{t("dash.ram_usage")}</span>
                                <span className="text-blue-600 dark:text-blue-400 transition-colors">{status.system?.ram || 0}%</span>
                            </div>
                            <div className="w-full h-2 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden transition-colors">
                                <div
                                    className="h-full bg-blue-500 rounded-full transition-all duration-1000"
                                    style={{ width: `${status.system?.ram || 0}%` }}
                                ></div>
                            </div>
                        </div>

                        <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 mt-auto">
                            <div className="flex gap-3">
                                <div className="mt-1 text-amber-600 dark:text-amber-500">
                                    <Activity size={16} />
                                </div>
                                <div>
                                    <p className="text-xs font-bold text-amber-600 dark:text-amber-500 uppercase mb-1">Mantenimiento</p>
                                    <p className="text-xs text-slate-600 dark:text-slate-400">Sistema operativo y estable.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {/* Detail Modal */}
            {
                selectedAlert && (
                    <div className="fixed inset-0 bg-slate-900/80 dark:bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in duration-200" onClick={() => setSelectedAlert(null)}>
                        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-white/10 rounded-2xl p-6 max-w-lg w-full shadow-2xl space-y-4" onClick={e => e.stopPropagation()}>
                            <div className="flex justify-between items-start">
                                <div>
                                    <h3 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2 transition-colors">
                                        {selectedAlert.event.includes("Caída") ? <AlertTriangle className="text-rose-500" /> : <Video className="text-indigo-500" />}
                                        {selectedAlert.event}
                                    </h3>
                                    <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">{selectedAlert.date} • {selectedAlert.camera}</p>
                                </div>
                                <button onClick={() => setSelectedAlert(null)} className="text-slate-400 hover:text-slate-900 dark:hover:text-white p-1 rounded-full hover:bg-slate-100 dark:hover:bg-white/10 transition-colors">
                                    <X size={20} />
                                </button>
                            </div>

                            <div className="bg-slate-100 dark:bg-black/40 rounded-xl p-4 border border-slate-200 dark:border-white/5">
                                <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Detalles del Envío</h4>
                                <p className="text-sm text-slate-700 dark:text-slate-300 font-mono whitespace-pre-wrap">
                                    {selectedAlert.details}
                                </p>
                            </div>

                            {selectedAlert.snapshot && (
                                <div className="rounded-xl overflow-hidden border border-slate-200 dark:border-white/10 bg-black">
                                    <img src={`http://127.0.0.1:8001/${selectedAlert.snapshot}`} alt="Snapshot" className="w-full object-cover" />
                                </div>
                            )}

                            <div className="flex justify-end pt-2">
                                <span className={`px-3 py-1 rounded-full text-xs font-bold ${selectedAlert.status === "Enviado" ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20" : "bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20"
                                    }`}>
                                    {t("alerts.table.status")}: {selectedAlert.status}
                                </span>
                            </div>
                        </div>
                    </div>
                )
            }
        </div >
    );
};

export default Dashboard;
