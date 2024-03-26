const express = require('express');
const router = express.Router();
const User = require('../models/user');

// GET: Listar usuários
router.get('/',  async (req, res) => {
  try {
    const users = await User.findAll();
    res.json(users);
  } catch (error) {
    res.status(500).send(error.message);
  }
});

// GET: Listar usuários
router.get('/:id', async (req, res) => {
  try {
    const user = await User.findByPk(req.params.id);
    res.json(user);
  } catch (error) {
    res.status(500).send(error.message);
  }
});

// Dentro de routes/users.js ou similar
router.post('/', async (req, res) => {
  try {
    console.log(req.body);
    // console.log(req);
    const user = await User.create(req.body);
    res.status(201).json(user);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});


// Dentro de routes/users.js ou similar
router.put('/:id', async (req, res) => {
  try {
    const user = await User.findByPk(req.params.id);
    if (user) {
      await user.update(req.body);
      res.json(user);
    } else {
      res.status(404).json({ message: 'Usuário não encontrado.' });
    }
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

// Dentro de routes/users.js ou similar
router.delete('/:id', async (req, res) => {
  try {
    const user = await User.findByPk(req.params.id);
    if (user) {
      await user.destroy();
      res.json({ message: 'Usuário removido com sucesso.'});
    } else {
      res.status(404).json({ message: 'Usuário não encontrado.' });
    }
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});


module.exports = router;
