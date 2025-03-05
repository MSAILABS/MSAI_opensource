import Records from "./records";
import Links from "../_components/links";

export default function page() {
  return (
    <div className="main_screen h-screen">
      <Links />
      <Records />
    </div>
  );
}
