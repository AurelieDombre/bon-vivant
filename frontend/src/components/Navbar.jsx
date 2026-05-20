import { NavLink } from "react-router-dom";


function Navbar() {
  // Barre de navigation simple pour passer du chatbot
  // a la page upsell.
  const linkClassName = ({ isActive }) =>
    `rounded-lg px-3 py-2 text-sm font-medium transition ${
      isActive
        ? "bg-zinc-900 text-white"
        : "text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900"
    }`;

  return (
    <header className="border-b border-zinc-200 bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <div>
          <h1 className="text-lg font-semibold text-zinc-900">
            Bon Vivant
          </h1>
        </div>

        <nav className="flex items-center gap-2">
          <NavLink to="/" end className={linkClassName}>
            Chat
          </NavLink>
          <NavLink to="/upsell" className={linkClassName}>
            Upsell
          </NavLink>
          <NavLink to="/newsletter" className={linkClassName}>
            Newsletters
          </NavLink>
        </nav>
      </div>
    </header>
  );
}

export default Navbar;
