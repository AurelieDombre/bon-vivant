import { BrowserRouter, Route, Routes } from "react-router-dom";

import Navbar from "./components/Navbar";
import ChatPage from "./pages/ChatPage";
import UpsellPage from "./pages/UpsellPage";


function App() {
  // App.jsx ne gere plus directement l'UI du chat.
  // Son role est maintenant de definir la navigation entre les pages.
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-zinc-50">
        <Navbar />

        <main className="flex justify-center py-8">
          <Routes>
            <Route path="/" element={<ChatPage />} />
            <Route path="/upsell" element={<UpsellPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
