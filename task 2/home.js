import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

const Home = () => {
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5000/recipes").then((response) => {
      setRecipes(response.data);
    });
  }, []);

  return (
    <div>
      <h1>Recipe Sharing Platform</h1>
      {recipes.map((recipe) => (
        <div key={recipe._id} className="recipe">
          <h2>{recipe.title}</h2>
          <p>{recipe.description}</p>
          <Link to={`/recipe/${recipe._id}`}>View Recipe</Link>
        </div>
      ))}
    </div>
  );
};

export default Home;
