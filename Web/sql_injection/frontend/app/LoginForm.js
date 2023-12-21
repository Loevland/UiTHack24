"use client";

import { useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function LoginForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userCredentials = { username, password };

    console.log("userCredentials");
    console.log(userCredentials);

    try {
      const response = await fetch("http://localhost:5000/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `username=${encodeURIComponent(
          username
        )}&password=${encodeURIComponent(password)}`,
      });
    

      console.log("response");
      console.log(response);

      const responseText = await response.text();
      console.log("responseText");
      console.log(responseText);
      
      if(responseText === "Login failed!"){
        throw new Error("Login failed");
      }
      else if(responseText === "Naughty naughty!")
      {
        toast.warning(responseText, {
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          draggable: true,
        });
      }
      else
      {
        toast.success(responseText, {
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          draggable: true,
        });
      }



      if (!response.ok) {
        throw new Error("Login failed");
      }



      // Handle successful login here
    } catch (error) {
      toast.error("Login failed", {
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        draggable: true,
      });
    }
  };

  return (
    <form
      className="flex flex-col items-center justify-center min-h-screen"
      onSubmit={handleSubmit}
    >
      <div className="flex flex-col">
        <label className="mb-2">
          Username:
          <input
            className="border p-2 rounded"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </label>
        <label className="mb-2">
          Password:
          <input
            className="border p-2 rounded"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        <input
          className="bg-blue-500 text-white p-2 rounded mt-4"
          type="submit"
          value="Submit"
        />
      </div>
      <ToastContainer />
    </form>
  );
}

export default LoginForm;
