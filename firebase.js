// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyA5HME7SOlbEIppjEq83pPBpfzac3OSnF4",
  authDomain: "health-15af2.firebaseapp.com",
  databaseURL: "https://health-15af2-default-rtdb.firebaseio.com",
  projectId: "health-15af2",
  storageBucket: "health-15af2.appspot.com",
  messagingSenderId: "585133503410",
  appId: "1:585133503410:web:c3541abc164273288b6aab",
  measurementId: "G-H436SFDGDG"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);