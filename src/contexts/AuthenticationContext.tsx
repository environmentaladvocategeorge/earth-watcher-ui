import React, { createContext, useState, useContext, ReactNode } from "react";
import { authenticateUser } from "@/lib/cognito";
import { CognitoUserSession } from "amazon-cognito-identity-js";

interface AuthContextType {
  user: CognitoUserSession | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  showLoginModal: boolean;
  setShowLoginModal: (value: boolean) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<CognitoUserSession | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);

  const login = async (username: string, password: string): Promise<void> => {
    return new Promise<void>((resolve, reject) => {
      authenticateUser(
        username,
        password,
        (err: Error | null, result: CognitoUserSession | null) => {
          if (err) {
            console.error("Login failed", err);
            reject(err);
          } else {
            console.log("Login success", result);
            setUser(result);
            setIsAuthenticated(true);
            setShowLoginModal(false);
            resolve();
          }
        }
      );
    });
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    setShowLoginModal(true);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        logout,
        isAuthenticated,
        showLoginModal,
        setShowLoginModal,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};