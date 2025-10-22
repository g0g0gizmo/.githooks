// popup.js
// Shows error and warning messages in browser (alert), Node.js CLI (console.error with color if available), and as a native popup (node-notifier)
//
// To enable Node.js popups, install node-notifier:
//   npm install node-notifier
// popup.js
// Shows error and warning messages in browser (alert), Node.js CLI (console.error with color if available), and as a native popup or notification.
//
// To enable Node.js popups/notifications, install node-notifier:
//   npm install node-notifier
//
// On Linux, zenity is used as a fallback for popups if node-notifier is not available.

let chalk = null;
let notifier = null;
const { execSync } = require('child_process');
try {
  chalk = require('chalk');
} catch (e) {
  // chalk not available, fallback to plain output
}
try {
  notifier = require('node-notifier');
} catch (e) {
  // node-notifier not available, fallback to zenity or alert
}

function isLinux() {
  return process && process.platform === 'linux';
}

function tryZenity(type, title, message) {
  // Only works on Linux with zenity installed
  if (!isLinux()) return false;
  try {
    execSync(`zenity --${type} --title="${title}" --text="${message.replace(/"/g, '\"')}"`, { stdio: 'ignore' });
    return true;
  } catch (e) {
    return false;
  }
}

function showPopup(type, title, message) {
  // Browser popup
  if (typeof window !== 'undefined' && typeof window.alert === 'function') {
    window.alert(`${title}: ${message}`);
    return;
  }
  // Node.js popup/notification
  if (notifier) {
    notifier.notify({
      title: title,
      message: message,
      wait: false
    });
    return;
  }
  // Linux fallback: zenity
  if (isLinux()) {
    let zenityType = type === 'error' ? 'error' : 'notification';
    if (tryZenity(zenityType, title, message)) return;
  }
  // Fallback: just print to console
  if (type === 'error') {
    console.error(`${title}: ${message}`);
  } else {
    console.log(`${title}: ${message}`);
  }
}

function showError(message) {
  // Always print to stdout
  if (chalk) {
    console.log(chalk.red.bold('Error: ') + chalk.red(message));
  } else {
    console.log('Error: ' + message);
  }
  // Always print to stderr
  if (chalk) {
    console.error(chalk.red.bold('Error: ') + chalk.red(message));
  } else {
    console.error('Error: ' + message);
  }
  // Always show a popup for errors
  showPopup('error', 'Error', message);
}

function showWarning(message) {
  // Always print to stdout
  if (chalk) {
    console.log(chalk.yellow.bold('Warning: ') + chalk.yellow(message));
  } else {
    console.log('Warning: ' + message);
  }
  // Always print to stderr
  if (chalk) {
    console.error(chalk.yellow.bold('Warning: ') + chalk.yellow(message));
  } else {
    console.error('Warning: ' + message);
  }
  // Prefer taskbar notification for warnings, fallback to popup
  showPopup('notification', 'Warning', message);
}

module.exports = { showError, showWarning };

function showWarning(message) {
  // Always print to stdout
  if (chalk) {
    console.log(chalk.yellow.bold('Warning: ') + chalk.yellow(message));
  } else {
    console.log('Warning: ' + message);
  }

  // Always print to stderr
  if (chalk) {
    console.error(chalk.yellow.bold('Warning: ') + chalk.yellow(message));
  } else {
    console.error('Warning: ' + message);
  }

  // Show popup for this warning
  showPopup('Warning', message);
}

module.exports = { showError, showWarning };