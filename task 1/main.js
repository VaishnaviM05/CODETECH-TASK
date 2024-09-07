const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

// Connect to MongoDB
mongoose.connect('mongodb://localhost/portfolio', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Project Schema and Model
const ProjectSchema = new mongoose.Schema({
  title: String,
  description: String,
  link: String,
  date: { type: Date, default: Date.now },
});

const Project = mongoose.model('Project', ProjectSchema);

// API Routes
app.get('/projects', async (req, res) => {
  const projects = await Project.find();
  res.json(projects);
});

app.post('/projects', async (req, res) => {
  const newProject = new Project(req.body);
  await newProject.save();
  res.json(newProject);
});

app.listen(5000, () => {
  console.log('Server running on port 5000');
});
