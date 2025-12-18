import { useEffect, useState } from 'react';
import { Activity, ShieldCheck, HardDrive, Wifi, Video } from 'lucide-react';

// eslint-disable-next-line no-unused-vars
const StatCard = ({ title, value, icon: Icon, color, trend }) => (
    <div className="glass-panel p-6 rounded-2xl relative overflow-hidden group hover:-translate-y-1 transition-transform duration-300">
        <div className={`absolute -right-6 -top-6 w-24 h-24 rounded-full opacity-10 blur-xl ${color}`}></div>

        <div className="flex justify-between items-start mb-4 relative z-10">
            <div className={`p-3 rounded-xl bg-white/5 border border-white/10 ${color.replace('bg-', 'text-')}`}>
                <Icon size={24} />
            </div>
            {trend && (
                <span className={`text-xs px-2 py-1 rounded-full border ${trend > 0
                        ? 'border-emerald-500/20 text-emerald-400 bg-emerald-500/10'
                        : 'border-rose-500/20 text-rose-400 bg-rose-500/10'
                    }`}>
                    {trend > 0 ? '+' : ''}{trend}%
                </span>
            )}
        </div>

        <div className="relative z-10">
            <h3 className="text-slate-400 text-sm font-medium mb-1">{title}</h3>
            <p className="text-3xl font-bold text-white tracking-tight">{value}</p>
        </div>
    </div>
);

const Dashboard = () => {
    const [status, setStatus] = useState({ connected: false, camera_status: 'Checking...' });
    const [date, setDate] = useState(new Date());

    useEffect(() => {
        const timer = setInterval(() => setDate(new Date()), 60000);
        return () => clearInterval(timer);
    }, []);

    useEffect(() => {
        const interval = setInterval(() => {
            fetch('http://127.0.0.1:8001/status')
                .then(res => res.json())
                .then(data => setStatus(data))
                .catch(() => setStatus({ connected: false, camera_status: 'Offline' }));
        }, 2000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            {/* Header */}
            <header className="flex justify-between items-end">
                <div>
                    <h2 className="text-4xl font-bold text-white mb-2 tracking-tight">Dashboard</h2>
                    <p className="text-slate-400">Visión general del sistema de vigilancia.</p>
                </div>
                <div className="text-right glass-panel px-4 py-2 rounded-xl">
                    <p className="text-sm font-medium text-slate-300">
                        {date.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long' })}
                    </p>
                    <p className="text-xs text-slate-500 uppercase tracking-widest">
                        {date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}
                    </p>
                </div>
            </header>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title="Estado del Sistema"
                    value={status.connected ? "Online" : "Offline"}
                    icon={Wifi}
                    color={status.connected ? "bg-emerald-500" : "bg-rose-500"}
                />
                <StatCard
                    title="Cámara"
                    value={status.camera_status}
                    icon={Activity}
                    color="bg-blue-500"
                />
                <StatCard
                    title="Amenazas"
                    value="0"
                    icon={ShieldCheck}
                    color="bg-amber-500"
                    trend={-5}
                />
                <StatCard
                    title="Almacenamiento"
                    value="45%"
                    icon={HardDrive}
                    color="bg-purple-500"
                    trend={12}
                />
            </div>

            {/* Bento Grid layout for bottom section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Recent Activity */}
                <div className="lg:col-span-2 glass-panel p-6 rounded-2xl border-white/5">
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="text-xl font-bold text-white">Actividad Reciente</h3>
                        <button className="text-xs text-blue-400 hover:text-blue-300 transition-colors">Ver todo</button>
                    </div>

                    <div className="space-y-4">
                        {[1, 2, 3].map(i => (
                            <div key={i} className="group flex items-center justify-between p-4 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 transition-all cursor-pointer">
                                <div className="flex items-center gap-4">
                                    <div className="w-12 h-12 rounded-full bg-indigo-500/20 flex items-center justify-center text-indigo-400 group-hover:scale-110 transition-transform">
                                        <Video size={20} />
                                    </div>
                                    <div>
                                        <p className="text-white font-medium">Movimiento detectado</p>
                                        <p className="text-xs text-slate-400">Cámara Principal • Hace {i * 5} min</p>
                                    </div>
                                </div>
                                <span className="text-xs text-slate-500 bg-black/30 px-3 py-1 rounded-lg group-hover:text-blue-400 transition-colors">
                                    Revisar
                                </span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Server Status */}
                <div className="glass-panel p-6 rounded-2xl border-white/5 flex flex-col">
                    <h3 className="text-xl font-bold text-white mb-6">Estado de Servidores</h3>

                    <div className="space-y-6 flex-1">
                        <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                                <span className="text-slate-400">Backend API</span>
                                <span className={status.connected ? "text-emerald-400" : "text-rose-400"}>
                                    {status.connected ? '98%' : 'Errors'}
                                </span>
                            </div>
                            <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                                <div
                                    className={`h-full rounded-full ${status.connected ? 'bg-emerald-500' : 'bg-rose-500'} transition-all duration-1000`}
                                    style={{ width: status.connected ? '98%' : '5%' }}
                                ></div>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                                <span className="text-slate-400">Database</span>
                                <span className="text-emerald-400">100%</span>
                            </div>
                            <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                                <div className="h-full bg-blue-500 rounded-full w-full"></div>
                            </div>
                        </div>

                        <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 mt-auto">
                            <div className="flex gap-3">
                                <div className="mt-1 text-amber-500">
                                    <Activity size={16} />
                                </div>
                                <div>
                                    <p className="text-xs font-bold text-amber-500 uppercase mb-1">Mantenimiento</p>
                                    <p className="text-xs text-slate-400">Programado para mañana a las 03:00 AM. El sistema se reiniciará.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};



export default Dashboard;
