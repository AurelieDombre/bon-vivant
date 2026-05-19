import Upsell from "../components/Upsell";


function UpsellPage() {
  // Page container :
  // elle se contente ici d'encadrer le composant Upsell.
  return (
    <div className="flex w-full max-w-4xl flex-col gap-6 px-4">
      <div>
        <h2 className="text-3xl font-bold text-zinc-900">
          Upsell
        </h2>
        <p className="text-sm text-zinc-600">
          Exemple de proposition commerciale complementaire pilotée par l'API.
        </p>
      </div>

      <Upsell />
    </div>
  );
}

export default UpsellPage;
