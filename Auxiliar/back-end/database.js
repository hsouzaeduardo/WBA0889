// database.js
const { Sequelize } = require('sequelize');
const sequelize = new Sequelize('sqlite:./database.sqlite');
module.exports = sequelize;
