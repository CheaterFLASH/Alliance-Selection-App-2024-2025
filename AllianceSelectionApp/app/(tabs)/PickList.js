import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  LayoutAnimation,
  UIManager,
  Platform,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import allTeams from '../data/teamsData'; // Update this line

// Enable LayoutAnimation on Android
if (Platform.OS === 'android' && UIManager.setLayoutAnimationEnabledExperimental) {
  UIManager.setLayoutAnimationEnabledExperimental(true);
}

const PickList = () => {
  const [teams, setTeams] = useState([]);
  const [teamInput, setTeamInput] = useState('');

  useEffect(() => {
    const loadTeams = async () => {
      try {
        const savedTeams = Platform.OS === 'web'
          ? JSON.parse(localStorage.getItem('teams')) || []
          : JSON.parse(await AsyncStorage.getItem('teams')) || [];
        setTeams(savedTeams);
      } catch (error) {
        console.error('Failed to load teams', error);
      }
    };

    loadTeams();
  }, []);

  useEffect(() => {
    const saveTeams = async () => {
      try {
        const teamsString = JSON.stringify(teams);
        if (Platform.OS === 'web') {
          localStorage.setItem('teams', teamsString);
        } else {
          await AsyncStorage.setItem('teams', teamsString);
        }
      } catch (error) {
        console.error('Failed to save teams', error);
      }
    };

    saveTeams();
  }, [teams]);

  const handleAddTeam = () => {
    if (!teamInput.trim()) return;

    const existingTeam = allTeams.find(team => team.name === `Team ${teamInput.trim()}`);
    if (!existingTeam) {
      alert('Team not found in the total list');
      return;
    }

    // Check if team is already in the pick list
    const isDuplicate = teams.some(team => team.number === teamInput.trim());
    if (isDuplicate) {
      alert('This team is already in your pick list');
      setTeamInput('');
      return;
    }

    const newTeam = {
      id: existingTeam.id,
      number: teamInput.trim(),
      rank: teams.length + 1
    };

    setTeams([...teams, newTeam]);
    setTeamInput('');
  };

  const handleResetTeams = () => {
    setTeams([]);
    if (Platform.OS === 'web') {
      localStorage.removeItem('teams');
    } else {
      AsyncStorage.removeItem('teams');
    }
  };

  const moveTeam = (index, direction) => {
    const newTeams = [...teams];
    const targetIndex = index + direction;

    if (targetIndex < 0 || targetIndex >= newTeams.length) return;

    if (Platform.OS !== 'web') {
      LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
    }

    const [movedTeam] = newTeams.splice(index, 1);
    newTeams.splice(targetIndex, 0, movedTeam);

    setTeams(newTeams.map((team, idx) => ({ ...team, rank: idx + 1 })));
  };

  const renderItem = ({ item, index }) => {
    return (
      <View style={styles.teamItem}>
        <Text style={styles.rankNumber}>{item.rank}</Text>
        <Text style={styles.teamNumber}>Team {item.number}</Text>
        <View style={styles.arrowContainer}>
          <TouchableOpacity onPress={() => moveTeam(index, -1)}>
            <Text style={styles.arrow}>↑</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={() => moveTeam(index, 1)}>
            <Text style={styles.arrow}>↓</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={teamInput}
          onChangeText={setTeamInput}
          placeholder="Enter team number"
          keyboardType="numeric"
          returnKeyType="done"
          onSubmitEditing={handleAddTeam}
        />
        <TouchableOpacity 
          style={styles.addButton}
          onPress={handleAddTeam}
        >
          <Text style={styles.addButtonText}>Add</Text>
        </TouchableOpacity>
        <TouchableOpacity 
          style={styles.resetButton}
          onPress={handleResetTeams}
        >
          <Text style={styles.resetButtonText}>Reset</Text>
        </TouchableOpacity>
      </View>

      {teams.map((item, index) => (
        <View key={item.id || index}>
          {renderItem({ item, index })}
        </View>
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#f5f5f5',
  },
  inputContainer: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  input: {
    flex: 1,
    backgroundColor: 'white',
    padding: 12,
    borderRadius: 8,
    marginRight: 8,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  addButton: {
    backgroundColor: '#2196f3',
    padding: 12,
    borderRadius: 8,
    justifyContent: 'center',
    marginRight: 8,
  },
  addButtonText: {
    color: 'white',
    fontWeight: 'bold',
  },
  resetButton: {
    backgroundColor: '#f44336',
    padding: 12,
    borderRadius: 8,
    justifyContent: 'center',
  },
  resetButtonText: {
    color: 'white',
    fontWeight: 'bold',
  },
  teamItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'white',
    padding: 16,
    marginBottom: 12,
    borderRadius: 8,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
  },
  rankNumber: {
    fontWeight: 'bold',
    marginRight: 16,
    width: 30,
  },
  teamNumber: {
    flex: 1,
    fontSize: 16,
  },
  arrowContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'flex-end',
  },
  arrow: {
    fontSize: 18,
    marginHorizontal: 8,
  },
});

export default PickList;