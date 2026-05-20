import { useState } from "react";


// Mini-liste locale pour la demo.
// Elle permet de remplir rapidement le panier sans backend catalogue.
const PRODUCTS = [
  { label: "Brunch Estival", emoji: "🍳" },
  { label: "Jus de Raisin", emoji: "🍇" },
  { label: "Pinot Noir", emoji: "🍷" },
  { label: "Brunch Saint Valentin", emoji: "🌹" },
  { label: "Fromage de Chevre", emoji: "🧀" },
  { label: "Biere sans alcool", emoji: "🍺" },
];


function Upsell() {
  // Contenu courant du panier.
  const [cart, setCart] = useState([]);

  // Valeur du champ d'ajout manuel.
  const [input, setInput] = useState("");

  // Etat de chargement pendant l'appel API.
  const [loading, setLoading] = useState(false);

  // Suggestion renvoyee par le backend upsell.
  const [suggestion, setSuggestion] = useState("");

  // Message d'erreur simplifie pour l'interface.
  const [error, setError] = useState("");

  function handleQuickAdd(item) {
    if (!cart.includes(item)) {
      setCart([...cart, item]);
      setSuggestion("");
    }
  }

  function handleManualAdd(e) {
    e.preventDefault();

    if (input.trim() && !cart.includes(input.trim())) {
      setCart([...cart, input.trim()]);
      setInput("");
      setSuggestion("");
    }
  }

  function handleRemove(item) {
    setCart(cart.filter((c) => c !== item));
    setSuggestion("");
  }

  async function handleUpsell() {
    setError("");
    setSuggestion("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/upsell", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cart_items: cart }),
      });

      if (!response.ok) {
        throw new Error("Erreur serveur API");
      }

      const data = await response.json();
      setSuggestion(data.suggestion);
    } catch {
      setError("Une erreur est survenue.");
    }

    setLoading(false);
  }

  function handleAddSuggestion() {
    if (suggestion && !cart.includes(suggestion)) {
      setCart([...cart, suggestion]);
      setSuggestion("");
    }
  }

  return (
    <div className="rounded-lg border border-zinc-200 bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-2xl font-bold text-zinc-900">
        Votre panier
      </h2>

      {/* Affichage du panier sous forme de tags */}
      <div className="mb-4 flex min-h-[40px] flex-wrap gap-2">
        {cart.length === 0 && (
          <span className="italic text-zinc-400">Panier vide</span>
        )}

        {cart.map((item) => (
          <span
            key={item}
            className="flex items-center gap-1 rounded-2xl border border-zinc-200 bg-white px-4 py-2 text-lg font-medium text-zinc-800 shadow-sm"
          >
            <span className="text-xl">
              {PRODUCTS.find((p) => p.label === item)?.emoji || "🛒"}
            </span>
            {item}
            <button
              className="ml-2 cursor-pointer bg-transparent p-0 text-xl font-bold leading-none text-zinc-400 transition hover:text-red-600"
              onClick={() => handleRemove(item)}
              title="Retirer"
              type="button"
            >
              ×
            </button>
          </span>
        ))}
      </div>

      {/* Liste de produits rapides a ajouter */}
      <div className="mb-4 flex flex-wrap gap-2">
        {PRODUCTS.map((p) => (
          <button
            key={p.label}
            className={`flex items-center gap-2 rounded-xl border px-3 py-2 transition ${
              cart.includes(p.label)
                ? "border-green-300 bg-green-50 text-green-800"
                : "border-zinc-200 bg-white text-zinc-700 hover:bg-zinc-100"
            }`}
            onClick={() => handleQuickAdd(p.label)}
            disabled={cart.includes(p.label)}
          >
            <span className="text-xl">{p.emoji}</span>
            <span>{p.label}</span>
          </button>
        ))}
      </div>

      {/* Ajout manuel d'un produit libre */}
      <form onSubmit={handleManualAdd} className="mb-4 flex gap-2">
        <input
          className="flex-1 rounded-lg border border-zinc-300 p-2"
          placeholder="Ajouter autre produit..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button
          type="submit"
          className="rounded-lg bg-zinc-100 px-4 font-semibold text-zinc-900"
        >
          Ajouter
        </button>
      </form>

      {/* Bouton qui appelle l'API upsell */}
      <button
        onClick={handleUpsell}
        className="mb-2 w-full rounded-lg bg-blue-600 p-2 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
        disabled={loading || cart.length === 0}
      >
        {loading ? "Recherche IA..." : "Suggérer un produit complémentaire"}
      </button>

      {/* Affichage de la suggestion renvoyee par le backend */}
      {suggestion && (
        <div className="mt-4 flex items-center justify-between rounded border border-green-200 bg-green-50 p-3 text-green-900">
          <span>
            <b>Suggestion IA :</b> {suggestion}
          </span>
          <button
            onClick={handleAddSuggestion}
            className="ml-4 rounded bg-green-600 px-3 py-1 font-semibold text-white hover:bg-green-700"
          >
            Ajouter au panier
          </button>
        </div>
      )}

      {/* Message d'erreur simple si l'API repond mal */}
      {error && (
        <div className="mt-4 rounded border border-red-200 bg-red-50 p-3 text-red-900">
          {error}
        </div>
      )}
    </div>
  );
}

export default Upsell;
