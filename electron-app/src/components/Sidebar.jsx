import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Video, FileText, Camera, Settings, Activity } from 'lucide-react';

const Sidebar = () => {
    const navItems = [
        { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
        { name: 'Grabaciones', path: '/recordings', icon: Video },
        { name: 'Archivos', path: '/files', icon: FileText },
        { name: 'Test Cámara', path: '/camera-test', icon: Camera },
        { name: 'Configuración', path: '/settings', icon: Settings },
    ];

    return (
        <aside className="w-64 h-full flex flex-col p-4">
            {/* Header */}
            <div className="px-4 py-6 mb-4">
                <h1 className="text-2xl font-bold flex items-center gap-3 tracking-wider text-white">
                    <div className="relative flex items-center justify-center w-8 h-8 rounded-lg bg-blue-600/20 text-blue-400">
                        <Activity size={20} />
                        <div className="absolute inset-0 bg-blue-500/20 blur-md rounded-lg"></div>
                    </div>
                    <span>AINOMALY</span>
                </h1>
            </div>

            {/* Nav */}
            <nav className="flex-1 space-y-2">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `relative flex items-center gap-3 px-4 py-3.5 rounded-xl transition-all duration-300 group ${isActive
                                ? 'bg-blue-600/10 text-blue-400 shadow-[0_0_20px_-10px_rgba(59,130,246,0.5)]'
                                : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-white/5'
                            }`
                        }
                    >
                        {({ isActive }) => (
                            <>
                                <item.icon size={20} className={`transition-transform duration-300 ${isActive ? 'scale-110' : 'group-hover:scale-110'}`} />
                                <span className={`font-medium tracking-wide ${isActive ? 'font-semibold' : ''}`}>{item.name}</span>
                                {isActive && (
                                    <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-blue-500 rounded-r-full shadow-[0_0_10px_#3b82f6]"></div>
                                )}
                            </>
                        )}
                    </NavLink>
                ))}
            </nav>

            {/* Footer / Status */}
            <div className="mt-auto px-4 py-6">
                <div className="glass-panel p-4 rounded-xl flex items-center gap-3 border-none bg-white/5">
                    <div className="relative">
                        <span className="block w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                        <span className="absolute inset-0 rounded-full bg-emerald-500 blur-sm animate-pulse"></span>
                    </div>
                    <div>
                        <p className="text-xs font-semibold text-white">System Online</p>
                        <p className="text-[10px] text-emerald-400/80 tracking-wider">SECURE CONNECTION</p>
                    </div>
                </div>
            </div>
        </aside>
    );
};

export default Sidebar;
