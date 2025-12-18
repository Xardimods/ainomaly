import React from 'react';
import { Save } from 'lucide-react';

const Settings = () => {
    return (
        <div className="space-y-6 max-w-4xl animate-in fade-in duration-500">
            <header>
                <h2 className="text-3xl font-bold text-white mb-2 tracking-tight">Configuración</h2>
                <p className="text-slate-400">Ajustes generales de la aplicación y del sistema de IA.</p>
            </header>

            <section className="glass-panel rounded-2xl p-8 space-y-8 border-white/5">
                <div>
                    <h3 className="text-lg font-semibold mb-6 text-white flex items-center gap-2">
                        <span className="w-1 h-6 bg-blue-500 rounded-full shadow-[0_0_10px_#3b82f6]"></span>
                        General
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-300">Nombre del Dispositivo</label>
                            <input
                                type="text"
                                defaultValue="AInomaly-Station-1"
                                className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 outline-none focus:border-blue-500 focus:bg-blue-500/5 text-slate-200 transition-all placeholder:text-slate-600"
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-300">Idioma</label>
                            <select className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 outline-none focus:border-blue-500 focus:bg-blue-500/5 text-slate-200 transition-all appearance-none cursor-pointer">
                                <option className="bg-slate-900">Español</option>
                                <option className="bg-slate-900">English</option>
                            </select>
                        </div>
                    </div>
                </div>

                <hr className="border-white/5" />

                <div>
                    <h3 className="text-lg font-semibold mb-6 text-white flex items-center gap-2">
                        <span className="w-1 h-6 bg-emerald-500 rounded-full shadow-[0_0_10px_#10b981]"></span>
                        Detección de Anomalías
                    </h3>
                    <div className="space-y-4">
                        <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/5 hover:bg-white/10 transition-colors group cursor-pointer">
                            <span className="text-slate-300 font-medium">Sensibilidad de detección</span>
                            <input type="range" className="w-48 accent-blue-500 cursor-pointer" />
                        </div>
                        <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/5 hover:bg-white/10 transition-colors group cursor-pointer">
                            <span className="text-slate-300 font-medium group-hover:text-white transition-colors">Guardar clips automáticamente</span>
                            <div className="relative inline-flex items-center cursor-pointer">
                                <input type="checkbox" defaultChecked className="sr-only peer" />
                                <div className="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                            </div>
                        </div>
                        <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/5 hover:bg-white/10 transition-colors group cursor-pointer">
                            <span className="text-slate-300 font-medium group-hover:text-white transition-colors">Enviar notificaciones a Telegram</span>
                            <div className="relative inline-flex items-center cursor-pointer">
                                <input type="checkbox" className="sr-only peer" />
                                <div className="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="flex justify-end pt-4">
                    <button className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white px-8 py-3 rounded-xl font-medium transition-all shadow-lg shadow-blue-900/40 flex items-center gap-2 hover:-translate-y-0.5">
                        <Save size={18} />
                        Guardar Cambios
                    </button>
                </div>
            </section>
        </div>
    );
};

export default Settings;
