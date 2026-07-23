import ChatWindow from "./components/ChatWindow.jsx";

export default function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 py-8 px-4 sm:px-6 lg:px-8">
      <div className="mx-auto flex h-screen w-full max-w-md flex-col gap-6 overflow-hidden">
        <div className="flex-1 overflow-hidden rounded-[36px] bg-slate-50 shadow-soft">
          <ChatWindow />
        </div>
      </div>
    </div>
  );
}
