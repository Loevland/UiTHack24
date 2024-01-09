import Image from "next/image";
import LoginForm from "./LoginForm";

export default function Home() {
  return (
    <div className="grid-cols-2">
      <h1 className="text-center text-blue-500 text-4xl font-bold">My Homepage</h1>
      <LoginForm />
   </div>
  )     
}
