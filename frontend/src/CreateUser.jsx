import { useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000"; // Your FastAPI backend URL

const CreateUser = ({ onUserCreated }) => {
  const [day, setDay] = useState("");
  const [date, setDate] = useState("");
  const [amount, setAmount] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/users/`, { day, date, amount });
      alert("Expense added successfully!");
      onUserCreated(); // Refresh expense list
      setDay("");
      setDate("");
      setAmount("");
    } catch (error) {
      alert("Error adding expense.");
    }
  };

  return (
    <div className="flex flex-col items-justify mt-10">
      <h2 className="text-2xl font-bold mb-4">Create Expense</h2>
      <form onSubmit={handleSubmit} className="flex space-x-4">
        <input
          type="text"
          placeholder="Day"
          value={day}
          onChange={(e) => setDay(e.target.value)}
          required
          className="border-2 border-gray-300 rounded-md p-2 focus:outline-none focus:border-blue-500"
        />
        <input
          type="date"
          placeholder="Date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          required
          className="border-2 border-gray-300 rounded-md p-2 focus:outline-none focus:border-blue-500"
        />
        <input
          type="number"
          placeholder="Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
          className="border-2 border-gray-300 rounded-md p-2 focus:outline-none focus:border-blue-500"
        />
        <button
          type="submit"
          className="bg-blue-500 text-white font-bold py-2 px-4 rounded-md hover:bg-blue-600 transition-colors"
        >
          Add Expense
        </button>
      </form>
    </div>
  );
};

export default CreateUser;