import { UserProvider } from '@auth0/nextjs-auth0/client';
import { FC, ReactNode } from 'react';
import { AuthProvider } from './AuthContext';
import { ViewProvider } from './ViewContext';

type ProviderComponent = FC<{ children: ReactNode }>;

export const combineComponents = (...components: ProviderComponent[]): ProviderComponent => {
  return components.reduce(
    (AccumulatedComponents, CurrentComponent) => {
      const CombinedComponent: ProviderComponent = ({ children }) => (
        <AccumulatedComponents>
          <CurrentComponent>{children}</CurrentComponent>
        </AccumulatedComponents>
      );
      return CombinedComponent;
    },
    ({ children }) => <>{children}</>,
  );
};


const providers = [
  AuthProvider,
  ViewProvider,
  UserProvider
]

export const AppContextProvider = combineComponents(...providers);