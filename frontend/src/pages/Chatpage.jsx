import { useState } from "react";


function ChatPage() {
  // Historique complet de la conversation.
  // Chaque message contient un role et un contenu a afficher.
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Bonjour, je peux t'aider a choisir un vin.",
    },
  ]);

  // Valeur courante du champ de saisie.
  const [message, setMessage] = useState("");

  // Etat de chargement pendant l'appel a l'API.
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    const trimmedMessage = message.trim();

    if (!trimmedMessage || isLoading) {
      return;
    }

    const userMessage = {
      role: "user",
      content: trimmedMessage,
    };

    // On affiche tout de suite le message utilisateur.
    setMessages((prev) => [...prev, userMessage]);
    setMessage("");
    setIsLoading(true);

    try {
      const res = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_message: trimmedMessage,
          }),
        }
      );

      if (!res.ok) {
        throw new Error("Erreur API");
      }

      const data = await res.json();

      // On ajoute la reponse du bot a l'historique.
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.recommendation,
          sentiment: data.sentiment,
          escalateToHuman: data.escalate_to_human,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Je n'ai pas pu recuperer la reponse du serveur.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // Permet d'envoyer le message avec la touche Entree.
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="flex w-full max-w-4xl flex-col gap-4 px-4">
      <div>
        <h2 className="text-3xl font-bold text-zinc-900">
          Chatbot Vin
        </h2>
        <p className="text-sm text-zinc-600">
          Recommandations, infos produit et analyse simple du message.
        </p>
      </div>

      <div className="flex h-[70vh] flex-col overflow-hidden rounded-lg border border-zinc-200 bg-white shadow-sm">
        {/* Zone qui affiche tout l'historique sous forme de bulles */}
        <div className="flex-1 space-y-4 overflow-y-auto p-4">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${
                msg.role === "user"
                  ? "justify-end"
                  : "justify-start"
              }`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-6 ${
                  msg.role === "user"
                    ? "rounded-br-md bg-zinc-900 text-white"
                    : "rounded-bl-md bg-zinc-100 text-zinc-900"
                }`}
              >
                <p>{msg.content}</p>

                {msg.role === "assistant" && msg.sentiment && (
                  <div className="mt-3 border-t border-zinc-300/70 pt-2 text-xs text-zinc-500">
                    <p>
                      <strong>Sentiment :</strong> {msg.sentiment}
                    </p>
                    <p>
                      <strong>Escalade humain :</strong>{" "}
                      {msg.escalateToHuman ? "Oui" : "Non"}
                    </p>
                  </div>
                )}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="max-w-[80%] rounded-2xl rounded-bl-md bg-zinc-100 px-4 py-3 text-sm text-zinc-500">
                Le chatbot ecrit...
              </div>
            </div>
          )}
        </div>

        {/* Zone de saisie du message */}
        <div className="border-t border-zinc-200 bg-zinc-50 p-4">
          <div className="flex gap-3">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Pose ta question..."
              className="flex-1 rounded-lg border border-zinc-300 bg-white px-3 py-2 text-sm text-zinc-900 outline-none transition focus:border-zinc-500"
            />

            <button
              onClick={sendMessage}
              disabled={isLoading}
              className="rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-60"
            >
              Envoyer
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChatPage;
