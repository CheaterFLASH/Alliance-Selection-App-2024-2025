import React, { createContext, useContext, useState } from 'react';

const PickListContext = createContext();

export function PickListProvider({ children }) {
  const [pickList, setPickList] = useState([]);

  const addToPickList = (team) => {
    setPickList(current => [...current, team]);
  };

  const removeFromPickList = (teamId) => {
    setPickList(current => current.filter(team => team.id !== teamId));
  };

  return (
    <PickListContext.Provider value={{ pickList, addToPickList, removeFromPickList }}>
      {children}
    </PickListContext.Provider>
  );
}

export function usePickList() {
  const context = useContext(PickListContext);
  if (!context) {
    throw new Error('usePickList must be used within a PickListProvider');
  }
  return context;
} 