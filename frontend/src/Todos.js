import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Todos = () => {
    const [todos, setTodos] = useState([]);

    useEffect(() => {
        // Fetch data from FastAPI
        fetch("http://localhost:8000/todos/")
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => setTodos(data))
            .catch(error => console.error("Error fetching todos:", error));
    }, []);

    return (
        <div>
            <h1>Todo List</h1>
            <ul>
                {todos.map((todo) => (
                    <li key={todo.id}>
                        <h2>{todo.title}</h2>
                        <p>{todo.description}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Todos;
