// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import {
  getAuth,
  GoogleAuthProvider,
  GithubAuthProvider,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signInWithPopup,
  signOut,
  onAuthStateChanged,
} from "firebase/auth";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDVXL_UUzbWriIQxyWIHVl98DTxlLr9W-w",
  authDomain: "job-board-994f3.firebaseapp.com",
  projectId: "job-board-994f3",
  storageBucket: "job-board-994f3.firebasestorage.app",
  messagingSenderId: "1015941622879",
  appId: "1:1015941622879:web:7b7598782634e7e2243fea",
  measurementId: "G-GP9Q47REG0",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);

// Auth providers
const googleProvider = new GoogleAuthProvider();
const githubProvider = new GithubAuthProvider();

// Configure providers
googleProvider.setCustomParameters({
  prompt: "select_account",
});

githubProvider.setCustomParameters({
  allow_signup: "true",
});

export {
  auth,
  googleProvider,
  githubProvider,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signInWithPopup,
  signOut,
  onAuthStateChanged,
};
