import { useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

const CreateTodo = () => {
  const [userId, setUserId] = useState("");
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/users/${userId}/todos/`, { title, description });
      alert("Todo created successfully!");
      setUserId("");
      setTitle("");
      setDescription("");
    } catch (error) {
      alert("Error creating todo.");
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Add a Comment</h2>
      <form onSubmit={handleSubmit} className="flex items-center space-x-4">
        <input
          type="number"
          placeholder="User ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          required
          className="border-2 border-gray-300 rounded-md p-2 focus:outline-none focus:border-blue-500"
        />
        <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          className="border-2 border-gray-300 rounded-md p-2 focus:outline-none focus:border-blue-500"
        />
        <input
          type="text"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
          className="border-2 border-gray-300 rounded-md p-2 focus:outline-none focus:border-blue-500"
        />
        <button
          type="submit"
          className="bg-blue-500 text-white rounded-md px-4 py-2 hover:bg-blue-600 transition"
        >
          Add
        </button>
      </form>
    </div>
  );
};

export default CreateTodo;
