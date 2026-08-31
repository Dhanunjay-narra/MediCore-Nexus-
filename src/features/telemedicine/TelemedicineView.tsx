import React, { useState } from 'react';
import {
  Video,
  Mic,
  MicOff,
  VideoOff,
  PhoneOff,
  MessageSquare,
  FileText,
  User,
  ShieldCheck,
  Sparkles,
  Send,
  Pill,
} from 'lucide-react';

export const TelemedicineView: React.FC = () => {
  const [isVideoOn, setIsVideoOn] = useState(true);
  const [isAudioOn, setIsAudioOn] = useState(true);
  const [isCallActive, setIsCallActive] = useState(false);
  const [chatMessages, setChatMessages] = useState([
    {
      sender: 'Dr. Sarah Chen, MD',
      text: 'Good morning Michael. How are your asthma symptoms after starting the Albuterol regimen?',
      time: '10:02 AM',
    },
    {
      sender: 'Michael Chang (Patient)',
      text: 'Much better! Wheezing has reduced during morning exercise.',
      time: '10:03 AM',
    },
  ]);
  const [newMsg, setNewMsg] = useState('');

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMsg.trim()) return;
    setChatMessages((prev) => [
      ...prev,
      {
        sender: 'Dr. Sarah Chen, MD',
        text: newMsg,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      },
    ]);
    setNewMsg('');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black text-white">Telemedicine Virtual Suite</h1>
            <span className="px-2.5 py-0.5 rounded-full bg-teal-500/10 text-teal-400 text-xs font-bold border border-teal-500/20">
              HIPAA Compliant WebRTC
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Encrypted HD video consultations, in-call clinical chart synchronization, and instant e-prescribing.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Video Stream Frame */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-2xl space-y-4 flex flex-col justify-between">
          <div className="relative aspect-video bg-slate-950 rounded-xl overflow-hidden border border-slate-800 flex items-center justify-center">
            {isCallActive ? (
              <div className="relative w-full h-full flex items-center justify-center bg-gradient-to-tr from-slate-950 via-slate-900 to-slate-950">
                {/* Simulated Remote Video Feed (Patient) */}
                <div className="text-center">
                  <div className="w-24 h-24 rounded-full bg-teal-500/20 text-teal-300 border-2 border-teal-500/40 flex items-center justify-center font-black text-3xl mx-auto mb-3 animate-pulse">
                    MC
                  </div>
                  <div className="text-white font-bold text-base">Michael Chang</div>
                  <div className="text-xs text-teal-400 font-mono">
                    Connected • Latency 24ms • 1080p WebRTC
                  </div>
                </div>

                {/* Self View (Doctor PIP) */}
                <div className="absolute bottom-4 right-4 w-36 h-24 bg-slate-800 border-2 border-teal-500/50 rounded-xl overflow-hidden shadow-2xl flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-xs font-bold text-white">Dr. Sarah Chen</div>
                    <div className="text-[10px] text-teal-400">Doctor (You)</div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center p-6 space-y-3">
                <div className="w-16 h-16 rounded-2xl bg-teal-500/10 text-teal-400 flex items-center justify-center mx-auto border border-teal-500/20">
                  <Video className="w-8 h-8" />
                </div>
                <h3 className="text-base font-bold text-white">
                  Scheduled Session: Michael Chang (MRN-2026-004129)
                </h3>
                <p className="text-xs text-slate-400 max-w-sm mx-auto">
                  Encrypted room token verified. Ready for video and audio streaming.
                </p>
                <button
                  onClick={() => setIsCallActive(true)}
                  className="px-6 py-2.5 bg-gradient-to-r from-teal-500 to-emerald-600 hover:from-teal-400 hover:to-emerald-500 text-slate-950 font-black rounded-xl text-xs shadow-lg shadow-teal-500/20 transition"
                >
                  Start Video Consultation Room
                </button>
              </div>
            )}
          </div>

          {/* Call Controls Toolbar */}
          {isCallActive && (
            <div className="flex items-center justify-center gap-3 py-2 bg-slate-950/80 rounded-xl border border-slate-800">
              <button
                onClick={() => setIsAudioOn(!isAudioOn)}
                className={`p-3 rounded-xl transition ${
                  isAudioOn ? 'bg-slate-800 text-white' : 'bg-red-500 text-white'
                }`}
              >
                {isAudioOn ? <Mic className="w-5 h-5" /> : <MicOff className="w-5 h-5" />}
              </button>
              <button
                onClick={() => setIsVideoOn(!isVideoOn)}
                className={`p-3 rounded-xl transition ${
                  isVideoOn ? 'bg-slate-800 text-white' : 'bg-red-500 text-white'
                }`}
              >
                {isVideoOn ? <Video className="w-5 h-5" /> : <VideoOff className="w-5 h-5" />}
              </button>
              <button
                onClick={() => setIsCallActive(false)}
                className="p-3 bg-red-600 hover:bg-red-500 text-white rounded-xl font-bold transition flex items-center gap-2 px-6"
              >
                <PhoneOff className="w-5 h-5" />
                <span className="text-xs">End Call</span>
              </button>
            </div>
          )}
        </div>

        {/* Secure In-Call Chat & Clinical Notes */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between h-[520px]">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <MessageSquare className="w-5 h-5 text-teal-400" />
                <h3 className="font-extrabold text-sm text-white">In-Call Secure Chat</h3>
              </div>
              <span className="text-[10px] font-bold text-teal-400 bg-teal-950 px-2 py-0.5 rounded border border-teal-800">
                E2EE Active
              </span>
            </div>

            {/* Message Stream */}
            <div className="mt-3 space-y-3 overflow-y-auto max-h-80 pr-1 text-xs">
              {chatMessages.map((msg, i) => (
                <div key={i} className="space-y-1">
                  <div className="flex items-center justify-between text-[10px] text-slate-400">
                    <span className="font-bold text-teal-300">{msg.sender}</span>
                    <span>{msg.time}</span>
                  </div>
                  <div className="bg-slate-800 border border-slate-700/80 rounded-xl p-2.5 text-slate-200">
                    {msg.text}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Chat Input */}
          <form onSubmit={handleSendMessage} className="mt-3 pt-3 border-t border-slate-800 flex gap-2">
            <input
              type="text"
              placeholder="Type message to patient..."
              value={newMsg}
              onChange={(e) => setNewMsg(e.target.value)}
              className="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-teal-500"
            />
            <button
              type="submit"
              className="p-2 bg-teal-500 hover:bg-teal-400 text-slate-950 rounded-xl font-bold transition"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
