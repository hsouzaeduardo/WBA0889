const express = require('express');
const bodyParser = require('body-parser');
const sequelize = require('./database');
const User = require('./models/user');
const usersRouter = require('./routes/users');
const cors = require('cors');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.json()); 

app.use(cors({
  origin: '*',
  methods: 'DELETE',
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
}));

app.use('/api/users', usersRouter);


// Testar a conexão com o banco de dados
sequelize.authenticate()
  .then(() => console.log('Conexão com o banco de dados estabelecida com sucesso.'))
  .catch(err => console.error('Erro ao conectar com o banco de dados:', err));

// Sincronizar modelos
sequelize.sync().then(() => console.log('Modelos sincronizados com o banco de dados.'));

app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}...`);
});
