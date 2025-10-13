// Node.js script to show a Windows notification
const notifier = require('node-notifier');
const args = process.argv.slice(2);
const title = args[0] || 'Git Hook';
const message = args[1] || 'Notification from git hook.';
notifier.notify({
  title: title,
  message: message,
  wait: false
});