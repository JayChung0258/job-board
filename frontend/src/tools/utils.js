/**
 * Generate a random username
 * @returns {string} A random username in the format: AdjectiveNounNumber
 */
export const generateRandomUsername = () => {
  const adjectives = [
    "Swift",
    "Bright",
    "Bold",
    "Quick",
    "Sharp",
    "Smart",
    "Cool",
    "Fast",
    "Clear",
    "Fresh",
    "Calm",
    "Keen",
    "Pure",
    "Wild",
    "Free",
    "Lucky",
    "Happy",
    "Sunny",
    "Brave",
    "Clever",
  ];

  const nouns = [
    "Developer",
    "Coder",
    "Designer",
    "Engineer",
    "Creator",
    "Builder",
    "Maker",
    "Thinker",
    "Innovator",
    "Expert",
    "Pro",
    "Ninja",
    "Wizard",
    "Hero",
    "Star",
    "Tiger",
    "Wolf",
    "Eagle",
    "Phoenix",
    "Dragon",
  ];

  const randomAdjective =
    adjectives[Math.floor(Math.random() * adjectives.length)];
  const randomNoun = nouns[Math.floor(Math.random() * nouns.length)];
  const randomNumber = Math.floor(Math.random() * 1000);

  return `${randomAdjective}${randomNoun}${randomNumber}`;
};

/**
 * Generate a random ID string
 * @param {number} length - Length of the ID (default: 8)
 * @returns {string} A random alphanumeric ID
 */
export const generateRandomId = (length = 8) => {
  const characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let result = "";
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
};

/**
 * Capitalize the first letter of a string
 * @param {string} str - String to capitalize
 * @returns {string} Capitalized string
 */
export const capitalize = (str) => {
  if (!str) return "";
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

/**
 * Format a date to a readable string
 * @param {Date|string} date - Date to format
 * @returns {string} Formatted date string
 */
export const formatDate = (date) => {
  if (!date) return "";
  const d = new Date(date);
  return d.toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

/**
 * Truncate text to a specified length
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length (default: 100)
 * @returns {string} Truncated text with ellipsis if needed
 */
export const truncateText = (text, maxLength = 100) => {
  if (!text) return "";
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength).trim() + "...";
};
