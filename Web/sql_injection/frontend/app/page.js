import Image from "next/image";
import LoginForm from "./LoginForm";
import "./page.css";

export default function Home() {
  return (
    <div className="flex justify-center items-center min-h-screen">
      <div className="bg-white border border-gray-200 rounded shadow-lg">
        <h1 className="matrix-style text-center text-blue-500 text-4xl font-bold mb-4">Login To Access Data</h1>
        <LoginForm />
      </div>
    </div>
  )
}
