import { Image, StyleSheet, Platform } from 'react-native';

import { HelloWave } from '@/components/HelloWave';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { Text } from "react-native"
import React, { useState } from 'react';
import {
 View,
 TouchableOpacity,
 ScrollView,

 Dimensions
} from 'react-native';

import AllianceSelection from './AllianceSelection'; // Ensure the file path is correct

export default function HomeScreen() {
  return (
    <AllianceSelection />
  );
}