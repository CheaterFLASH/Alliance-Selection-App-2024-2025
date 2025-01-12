import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { MaterialIcons } from '@expo/vector-icons';
import AllianceSelection from './(tabs)/AllianceSelection';
import PickList from './(tabs)/PickList';

const Tab = createBottomTabNavigator();

export default function Index() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarStyle: {
          backgroundColor: 'black',
        },
        tabBarActiveTintColor: 'white',
        tabBarInactiveTintColor: 'gray',
        // tabBarLabelStyle: {
        //     display: 'none'
        // }
      }}
    >
      <Tab.Screen 
        name="AllianceSelection" 
        component={AllianceSelection}
        options={{
          tabBarIcon: ({ color, size }) => (
            <MaterialIcons name="home" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen 
        name="PickList" 
        component={PickList}
        options={{
          tabBarIcon: ({ color, size }) => (
            <MaterialIcons name="edit" size={size} color={color} />
          ),
        }}
      />
    </Tab.Navigator>
  );
} 