import React from "react";
import { useAuth } from "../contexts/AuthContext";

const AuthStatus: React.FC = () => {
  const { currentUser, loading } = useAuth();

  if (loading) {
    return (
      <div className="text-sm text-gray-500">Checking authentication...</div>
    );
  }

  if (!currentUser) {
    return (
      <div className="text-sm text-gray-500 bg-gray-100 p-2 rounded">
        <strong>Status:</strong> Not authenticated
      </div>
    );
  }

  return (
    <div className="text-sm text-green-700 bg-green-100 p-2 rounded">
      <strong>Status:</strong> Authenticated as{" "}
      {currentUser.displayName || currentUser.email}
      <br />
      <strong>Provider:</strong>{" "}
      {currentUser.providerData[0]?.providerId || "email"}
      <br />
      <strong>UID:</strong> {currentUser.uid}
    </div>
  );
};

export default AuthStatus;
