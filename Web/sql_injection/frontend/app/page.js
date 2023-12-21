import Image from "next/image";
import LoginForm from "./LoginForm";

export default function Home() {
  return (
    <div>
      <h1 className="text-center">My Homepage</h1>
      <LoginForm />
    </div>
  );
}
