import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
  GithubAuthProvider,
  signOut,
  updateProfile,
  User,
} from "firebase/auth";
import { auth } from "../firebase_config";
import { generateRandomUsername } from "../tools/utils.js";

// Initialize providers
const googleProvider = new GoogleAuthProvider();
const githubProvider = new GithubAuthProvider();

// Configure Google provider
googleProvider.addScope("profile");
googleProvider.addScope("email");

// Configure GitHub provider
githubProvider.addScope("user:email");

export interface AuthError {
  code: string;
  message: string;
}

export interface SignUpData {
  email: string;
  password: string;
  displayName?: string;
}

export interface SignInData {
  email: string;
  password: string;
}

class AuthService {
  /**
   * Sign up with email and password
   */
  async signUpWithEmail({
    email,
    password,
    displayName,
  }: SignUpData): Promise<User> {
    try {
      const result = await createUserWithEmailAndPassword(
        auth,
        email,
        password,
      );

      // Generate random username if no display name provided
      const finalDisplayName = displayName || generateRandomUsername();

      // Update display name
      if (result.user) {
        await updateProfile(result.user, { displayName: finalDisplayName });
      }

      return result.user;
    } catch (error: any) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * Sign in with email and password
   */
  async signInWithEmail({ email, password }: SignInData): Promise<User> {
    try {
      const result = await signInWithEmailAndPassword(auth, email, password);
      return result.user;
    } catch (error: any) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * Sign in with Google
   */
  async signInWithGoogle(): Promise<User> {
    try {
      const result = await signInWithPopup(auth, googleProvider);
      return result.user;
    } catch (error: any) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * Sign in with GitHub
   */
  async signInWithGitHub(): Promise<User> {
    try {
      const result = await signInWithPopup(auth, githubProvider);
      return result.user;
    } catch (error: any) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * Sign out current user
   */
  async signOut(): Promise<void> {
    try {
      await signOut(auth);
    } catch (error: any) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * Get current user
   */
  getCurrentUser(): User | null {
    return auth.currentUser;
  }

  /**
   * Handle Firebase auth errors with user-friendly messages
   */
  private handleAuthError(error: any): AuthError {
    let message = "An unexpected error occurred";

    switch (error.code) {
      case "auth/user-not-found":
        message = "No account found with this email address";
        break;
      case "auth/wrong-password":
        message = "Incorrect password";
        break;
      case "auth/email-already-in-use":
        message = "An account with this email already exists";
        break;
      case "auth/weak-password":
        message = "Password should be at least 6 characters";
        break;
      case "auth/invalid-email":
        message = "Invalid email address";
        break;
      case "auth/user-disabled":
        message = "This account has been disabled";
        break;
      case "auth/too-many-requests":
        message = "Too many failed attempts. Please try again later";
        break;
      case "auth/popup-closed-by-user":
        message = "Sign-in was cancelled";
        break;
      case "auth/popup-blocked":
        message =
          "Popup was blocked by your browser. Please allow popups and try again";
        break;
      case "auth/account-exists-with-different-credential":
        message =
          "An account already exists with the same email but different sign-in credentials";
        break;
      default:
        message = error.message || "Authentication failed";
    }

    return {
      code: error.code || "auth/unknown",
      message,
    };
  }
}

export const authService = new AuthService();
