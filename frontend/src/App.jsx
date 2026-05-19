import { useState } from "react";


function App() {

  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  // Fonction appelée quand on clique sur Envoyer
  const sendMessage = async () => {

    // Requête POST vers FastAPI
    const res = await fetch(
      "http://127.0.0.1:8000/chat",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          user_message: message,
        }),
      }
    );

    // Conversion JSON
    const data = await res.json();

    // Mise à jour de la réponse
    setResponse(data.recommendation);
  };

  return (
    <div className="p-10">

      <h1 className="text-3xl font-bold mb-4">
        Chatbot Vin 🍷
      </h1>

      {/* Champ texte */}
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Pose ta question..."
        className="border p-2 w-full mb-4"
      />

      {/* Bouton */}
      <button onClick={sendMessage}>
        Envoyer
      </button>

      {/* Réponse IA */}
      <div className="mt-6">
        <h2 className="font-bold">
          Réponse :
        </h2>

        <p>{response}</p>
      </div>

    </div>
  );
}

export default App;