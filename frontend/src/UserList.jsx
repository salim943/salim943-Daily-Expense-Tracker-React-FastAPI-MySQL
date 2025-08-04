import { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

const UserList = () => {
  const [expenses, setExpenses] = useState([]);
  const [totalAmount, setTotalAmount] = useState(0);

  useEffect(() => {
    fetchExpenses();
  }, []);

  const fetchExpenses = async () => {
    try {
      const response = await axios.get(`${API_URL}/users/`);
      setExpenses(response.data);
      const total = response.data.reduce((sum, expense) => sum + parseFloat(expense.amount), 0);
      setTotalAmount(total);
    } catch (error) {
      alert("Error fetching expenses.");
    }
  };

  return (
    <div className="max-w-4xl mx-4 p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-2xl font-bold mb-4">Expenses</h2>
      <div className="mb-4 p-4 bg-blue-100 text-blue-800 font-semibold rounded-lg shadow-md">
        Total Amount: ${totalAmount.toFixed(2)}
      </div>
      <ul className="space-y-4">
        {expenses.map((expense) => (
          <li
            key={expense.id}
            className="border p-4 rounded-lg shadow-md bg-gray-100 hover:bg-gray-50 transition flex justify-between"
          >
            <p><strong>ID:</strong> {expense.id}</p>
            <p><strong>Day:</strong> {expense.day}</p>
            <p><strong>Date:</strong> {expense.date}</p>
            <p><strong>Amount:</strong> {expense.amount}</p>
            <p>{expense.todo ? `Comment: ${expense.todo.description}` : "No Comment"}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserList;
