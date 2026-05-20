import { useState } from "react";

const INTERESTS = [
{ label: "Vin", icon: "🍷" },
{ label: "Fromage", icon: "🧀" },
{ label: "Jazz", icon: "🎷" },
{ label: "Brunch", icon: "🥐" },
{ label: "Voyages", icon: "🌍" },
{ label: "Inspiration", icon: "💡" },
{ label: "Promotions", icon: "🎁" }
];

const WISHES = [
"Idées de recettes",
"Promotions exclusives",
"Inspiration pour brunch",
"Suggestions de soirées"
];

const FREQUENCIES = [
"1x/semaine",
"1x/mois",
"À chaque nouveauté"
];


export default function NewsletterIA() {
    const [selectedInterests, setSelectedInterests] = useState([])
    const [selectedWishes, setSelectedWishes] = useState([])
    const [frequency, setFrequency] = useState(FREQUENCIES[0])
    const [email, setEmail] = useState("")
    const [loading, setLoading] = useState(false);
    const [newsletter, setNewsletter] = useState("")
    const [error, setError] = useState(null);

    // Sélectionner / déselectionner un interet
    const toggleInterest = (label) => {
      setSelectedInterests(prev =>
        prev.includes(label)
          ? prev.filter(i => i !== label)
          : [...prev, label]
      )
    }
    // Sélection/déselection d’une envie
    const toggleWish = (wish) => {
        setSelectedWishes((prev) =>
            prev.includes(wish) ? prev.filter((w) => w !== wish) : [...prev, wish]
        )
    }
    // On envoie le formulaire
    const handleSubmit = async (e) => {

        e.preventDefault()
        setError("")
        setNewsletter("")
        setLoading(true)

        try{
            // Pour la démo, on ne passe que les intérêts
            const response = await fetch("http://localhost:8000/newsletter", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    interests: selectedInterests,
                    wishes: selectedWishes,
                    frequency: frequency,
                    email: email,
                })
            })
            if (!response.ok) throw new Error("Error API");
            const data = await response.json();
            setNewsletter(data.newsletter || data.text || "Aucune newsletter générée.");
        }catch (err){
            setError("Impossible de générer la newsletter.");
        }
        setLoading(false);
    };

    return (
        <div className="max-w-xl mx-auto p-8 bg-white rounded-2xl shadow-2xl mt-12">
            <h1 className="text-3xl font-semibold mb-1 text-center">Recevez votre newsletter <span className="font-bold text-green-700">Bon Vivant</span>, vraiment à votre image.</h1>
            <p className="text-center mb-6 text-gray-500">Personnalisez votre expérience :</p>
            <form onSubmit={handleSubmit} className="flex flex-col gap-5">
                {/* Centres d’intérêts : grille visuelle */}
                <div>
                    <label className="block mb-2 font-semibold">Vos centres d’intérêts</label>
                    <div className="grid grid-cols-4 gap-4">
                        {INTERESTS.map((item) => (
                        <button
                            type="button"
                            key={item.label}
                            className={`flex flex-col items-center justify-center rounded-xl border-2 h-20 text-2xl font-medium transition
                            ${selectedInterests.includes(item.label)
                              ? "bg-green-100 border-green-500 text-green-900"
                              : "bg-gray-50 border-gray-200 text-gray-500 hover:border-green-300"
                            }`}
                            onClick={() => toggleInterest(item.label)}
                        >
                            <span>{item.icon}</span>
                            <span className="text-xs mt-1">{item.label}</span>
                        </button>
                        ))}
                    </div>
                </div>

                {/* Envies (checkbox group) */}
                <div>
                    <label className="block mb-2 font-semibold">Que souhaitez-vous recevoir&nbsp;?</label>
                    <div className="flex flex-wrap gap-4">
                        {WISHES.map((wish) => (
                        <label key={wish} className="flex items-center gap-1 text-gray-700">
                        <input
                        type="checkbox"
                        checked={selectedWishes.includes(wish)}
                        onChange={() => toggleWish(wish)}
                        className="accent-green-600"
                        />
                        <span>{wish}</span>
                        </label>
                        ))}
                    </div>
                </div>

                {/* Fréquence */}
                <div>
                    <label className="block mb-2 font-semibold">Fréquence</label>
                    <select
                    className="border rounded p-2 w-full"
                    value={frequency}
                    onChange={(e) => setFrequency(e.target.value)}
                    >
                        {FREQUENCIES.map((freq) => (
                        <option key={freq} value={freq}>{freq}</option>
                        ))}
                    </select>
                </div>

                {/* Email */}
                <div>
                    <label className="block mb-2 font-semibold">Votre email</label>
                    <input
                        type="email"
                        className="border rounded p-2 w-full"
                        placeholder="nom@email.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>

                {/* Submit */}
                <button
                    type="submit"
                    className="bg-green-600 text-white rounded-lg p-3 font-semibold text-lg shadow hover:bg-green-700 transition"
                    disabled={loading || !selectedInterests.length || !email}
                >
                    {loading ? "Génération en cours…" : "Créer ma newsletter sur-mesure"}
                </button>
            </form>

            {/* Preview Newsletter */}
            {newsletter && (
                <div className="mt-6 p-4 rounded-xl bg-blue-50 border border-blue-200 text-blue-900 shadow-inner">
                <div className="font-bold mb-1 text-lg">Aperçu de votre newsletter personnalisée :</div>
                <div className="whitespace-pre-line">{newsletter}</div>
            </div>
            )}
            {error && (
                <div className="mt-4 p-3 rounded bg-red-50 border border-red-200 text-red-900">
                {error}
            </div>
            )}
        </div>
    )


}