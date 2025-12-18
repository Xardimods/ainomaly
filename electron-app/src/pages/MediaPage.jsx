import React, { useState, useEffect } from 'react';
import { Image, Video, Trash2, Download, Search, FileVideo, Play, X, Grid, List } from 'lucide-react';
import { useDialog } from '../context/DialogContext';
import { useLanguage } from '../context/LanguageContext';

const MediaPage = () => {
    const { t } = useLanguage();
    const { confirm, alert } = useDialog();
    const [activeTab, setActiveTab] = useState('all'); // 'all', 'images', 'videos'
    const [mediaItems, setMediaItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState("");
    const [selectedItem, setSelectedItem] = useState(null); // For lightingbox/modal

    // Fetch both snapshots and recordings
    const fetchMedia = async () => {
        setLoading(true);
        try {
            const [snapshotsRes, recordingsRes] = await Promise.all([
                fetch('http://127.0.0.1:8001/snapshots'),
                fetch('http://127.0.0.1:8001/recordings')
            ]);

            const snapshots = await snapshotsRes.json();
            const recordings = await recordingsRes.json();

            // Normalize data structure
            const normalizedSnapshots = snapshots.map(s => ({
                ...s,
                type: 'image',
                url: `http://127.0.0.1:8001${s.url}`, // Ensure full URL
                id: `img-${s.name}`
            }));

            const normalizedRecordings = recordings.map(r => ({
                ...r,
                type: 'video',
                url: `http://127.0.0.1:8001/recordings/${r.name}`,
                id: `vid-${r.name}`
            }));

            // Combine and sort by date/name (since date formats might differ, we'll try our best)
            // Ideally backend returns ISO dates, but here we have formatted strings.
            // For now, simpler to just concat.
            setMediaItems([...normalizedSnapshots, ...normalizedRecordings]);
        } catch (err) {
            console.error("Error fetching media:", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchMedia();
    }, []);

    const handleDelete = async (item, e) => {
        if (e) e.stopPropagation();

        const confirmed = await confirm(t("media.delete_confirm"), {
            variant: 'danger',
            confirmText: t("media.delete") || "Eliminar"
        });
        if (!confirmed) return;

        // If the item is currently open, close it
        if (selectedItem?.name === item.name) {
            setSelectedItem(null);
        }

        const endpoint = item.type === 'image'
            ? `http://127.0.0.1:8001/api/snapshots/${item.name}`
            : `http://127.0.0.1:8001/api/recordings/${item.name}`;

        try {
            // Unload if video is selected (handled by closing modal above)
            // Wait a tiny bit for UI lock release if needed
            await new Promise(r => setTimeout(r, 100));

            const res = await fetch(endpoint, { method: 'DELETE' });

            let result;
            if (res.ok) {
                result = { status: 'deleted' };
            } else {
                try {
                    result = await res.json();
                } catch {
                    result = { error: res.statusText };
                }
            }

            if (result.status === 'deleted') {
                setMediaItems(prev => prev.filter(i => i.id !== item.id));
            } else {
                const msg = result.error || result.detail || t("media.error_unknown");
                await alert(`${t("media.error_deleting")} ${msg}`, { variant: 'danger' });
            }
        } catch (err) {
            console.error("Error deleting:", err);
            await alert(t("media.error_connection"), { variant: 'danger' });
        }
    };

    const handleDownload = (item, e) => {
        if (e) e.stopPropagation();
        const link = document.createElement("a");
        link.href = item.url;
        link.download = item.name;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    // Filter Items
    const filteredItems = mediaItems.filter(item => {
        const matchesSearch = item.name.toLowerCase().includes(search.toLowerCase()) ||
            (item.date && item.date.toLowerCase().includes(search.toLowerCase()));
        const matchesTab = activeTab === 'all' ||
            (activeTab === 'images' && item.type === 'image') ||
            (activeTab === 'videos' && item.type === 'video');
        return matchesSearch && matchesTab;
    });

    return (
        <div className="space-y-6 animate-in fade-in duration-500 max-w-7xl mx-auto h-full flex flex-col">
            <header className="flex flex-col md:flex-row justify-between items-end gap-4">
                <div>
                    <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-2 tracking-tight transition-colors">{t("media.title")}</h2>
                    <p className="text-slate-500 dark:text-slate-400 transition-colors">{t("media.subtitle")}</p>
                </div>

                <div className="flex flex-col md:flex-row gap-4 w-full md:w-auto">
                    {/* Tabs */}
                    <div className="flex bg-slate-100 dark:bg-black/20 p-1 rounded-xl border border-slate-200 dark:border-white/10 transition-colors">
                        <button
                            onClick={() => setActiveTab('all')}
                            className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${activeTab === 'all' ? 'bg-white dark:bg-white/10 text-slate-900 dark:text-white shadow-sm' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'}`}
                        >
                            {t("media.tabs.all")}
                        </button>
                        <button
                            onClick={() => setActiveTab('videos')}
                            className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${activeTab === 'videos' ? 'bg-white dark:bg-indigo-500/20 text-indigo-600 dark:text-indigo-300 shadow-sm' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'}`}
                        >
                            <Video size={14} /> {t("media.tabs.videos")}
                        </button>
                        <button
                            onClick={() => setActiveTab('images')}
                            className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${activeTab === 'images' ? 'bg-white dark:bg-emerald-500/20 text-emerald-600 dark:text-emerald-300 shadow-sm' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'}`}
                        >
                            <Image size={14} /> {t("media.tabs.photos")}
                        </button>
                    </div>

                    {/* Search */}
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                        <input
                            type="text"
                            placeholder={t("media.search_placeholder")}
                            value={search}
                            onChange={e => setSearch(e.target.value)}
                            className="bg-white dark:bg-black/20 border border-slate-200 dark:border-white/10 rounded-xl pl-10 pr-4 py-2 text-slate-900 dark:text-white focus:outline-none focus:border-blue-500 w-full md:w-64 text-sm transition-colors"
                        />
                    </div>
                </div>
            </header>

            {loading ? (
                <div className="flex-1 flex items-center justify-center">
                    <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                </div>
            ) : (
                <div className="flex-1 overflow-y-auto pr-2">
                    {filteredItems.length > 0 ? (
                        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
                            {filteredItems.map((item) => (
                                <div
                                    key={item.id}
                                    onClick={() => setSelectedItem(item)}
                                    className={`group relative aspect-video bg-white dark:bg-black/40 rounded-xl overflow-hidden border transition-all cursor-pointer shadow-sm dark:shadow-none ${item.type === 'video' ? 'border-indigo-100 hover:border-indigo-300 dark:border-indigo-500/20 dark:hover:border-indigo-500/50' : 'border-emerald-100 hover:border-emerald-300 dark:border-emerald-500/20 dark:hover:border-emerald-500/50'
                                        }`}
                                >
                                    {/* Thumbnail / Preview */}
                                    {item.type === 'image' ? (
                                        <img
                                            src={item.url}
                                            alt={item.name}
                                            className="w-full h-full object-cover opacity-90 dark:opacity-80 group-hover:opacity-100 group-hover:scale-105 transition-all duration-500"
                                        />
                                    ) : (
                                        <div className="w-full h-full flex items-center justify-center bg-slate-100 dark:bg-slate-900 group-hover:scale-105 transition-transform duration-500">
                                            <video src={item.url} className="w-full h-full object-cover opacity-80 dark:opacity-60" />
                                            <div className="absolute inset-0 flex items-center justify-center">
                                                <div className="p-3 bg-white/30 dark:bg-white/10 backdrop-blur-md rounded-full text-white group-hover:bg-indigo-500 group-hover:scale-110 transition-all shadow-lg">
                                                    <Play size={20} fill="currentColor" />
                                                </div>
                                            </div>
                                        </div>
                                    )}

                                    {/* Overlay Info */}
                                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end p-3">
                                        <div className="flex items-center gap-2 mb-1">
                                            {item.type === 'video' ? <Video size={12} className="text-indigo-400" /> : <Image size={12} className="text-emerald-400" />}
                                            <p className="text-white text-xs font-medium truncate flex-1">{item.name}</p>
                                        </div>
                                        <p className="text-slate-300 text-[10px] mb-2">{item.date} • {item.size}</p>

                                        <div className="flex gap-2 justify-end">
                                            <button
                                                onClick={(e) => handleDownload(item, e)}
                                                className="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white transition-colors"
                                                title={t("media.download")}
                                            >
                                                <Download size={14} />
                                            </button>
                                            <button
                                                onClick={(e) => handleDelete(item, e)}
                                                className="p-1.5 rounded-lg bg-rose-500/20 hover:bg-rose-500/40 text-rose-400 transition-colors"
                                                title={t("media.delete")}
                                            >
                                                <Trash2 size={14} />
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="h-64 flex flex-col items-center justify-center text-slate-400 dark:text-slate-500 border-2 border-dashed border-slate-200 dark:border-white/5 rounded-2xl transition-colors">
                            <div className="p-4 bg-slate-100 dark:bg-white/5 rounded-full mb-4 transition-colors">
                                {activeTab === 'videos' ? <FileVideo size={32} /> : <Image size={32} />}
                            </div>
                            <p>{t("media.no_files")}</p>
                        </div>
                    )}
                </div>
            )}

            {/* Modal for Preview */}
            {selectedItem && (
                <div
                    className="fixed inset-0 z-50 bg-black/95 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-200"
                    onClick={() => setSelectedItem(null)}
                >
                    <button
                        className="absolute top-4 right-4 text-white/50 hover:text-white p-2 rounded-full hover:bg-white/10 transition-colors"
                        onClick={() => setSelectedItem(null)}
                    >
                        <X size={32} />
                    </button>

                    <div className="max-w-6xl max-h-[90vh] w-full flex flex-col gap-4" onClick={e => e.stopPropagation()}>
                        <div className="relative rounded-2xl overflow-hidden border border-white/10 shadow-2xl bg-black flex items-center justify-center h-[70vh]">
                            {selectedItem.type === 'image' ? (
                                <img
                                    src={selectedItem.url}
                                    alt={selectedItem.name}
                                    className="max-w-full max-h-full object-contain"
                                />
                            ) : (
                                <video
                                    src={selectedItem.url}
                                    controls
                                    autoPlay
                                    className="max-w-full max-h-full"
                                />
                            )}
                        </div>

                        <div className="flex justify-between items-center px-4 py-2 bg-white/5 rounded-xl border border-white/5">
                            <div>
                                <h3 className="text-white font-medium flex items-center gap-2">
                                    {selectedItem.type === 'video' ? <Video size={16} className="text-indigo-400" /> : <Image size={16} className="text-emerald-400" />}
                                    {selectedItem.name}
                                </h3>
                                <p className="text-slate-400 text-sm">{selectedItem.date} • {selectedItem.size}</p>
                            </div>
                            <div className="flex gap-3">
                                <button
                                    onClick={(e) => handleDownload(selectedItem, e)}
                                    className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-colors"
                                >
                                    <Download size={18} /> {t("media.download")}
                                </button>
                                <button
                                    onClick={(e) => handleDelete(selectedItem, e)}
                                    className="flex items-center gap-2 px-4 py-2 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 rounded-lg transition-colors border border-rose-500/20"
                                >
                                    <Trash2 size={18} /> {t("media.delete")}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default MediaPage;
