import React, { useState } from 'react';
import {
 View,
 Text,
 TouchableOpacity,
 ScrollView,
 StyleSheet,
 Dimensions
} from 'react-native';


// Minimal UI Components
const Card = ({ children, style, ...props }) => (
 <View style={[styles.card, style]} {...props}>
   {children}
 </View>
);


Card.Header = ({ children, style, ...props }) => (
 <View style={[styles.cardHeader, style]} {...props}>{children}</View>
);


Card.Title = ({ children, style, ...props }) => (
 <Text style={[styles.cardTitle, style]} {...props}>{children}</Text>
);


Card.Content = ({ children, style, ...props }) => (
 <View{...props}>{children}</View>
);


const Button = ({
 children,
 onPress,
 disabled,
 style,
 variant = 'outline',
 ...props
}) => {
 const variantStyles = {
   outline: styles.buttonOutline,
   secondary: styles.buttonSecondary
 };


 return (
   <TouchableOpacity
     onPress={onPress}
     disabled={disabled}
     style={[
       styles.button,
       variantStyles[variant],
       disabled && styles.buttonDisabled,
       style
     ]}
     {...props}
   >
     {children}
   </TouchableOpacity>
 );
};


const Alert = ({ children, variant = 'default', style, ...props }) => {
 const variantStyles = {
   destructive: styles.alertDestructive
 };


 return (
   <View
     style={[
       styles.alert,
       variantStyles[variant],
       style
     ]}
     {...props}
   >
     {children}
   </View>
 );
};


const AllianceSelection = () => {
 const generateRandomTeams = () => {
   return Array.from({ length: 34 }, (_, i) => ({
     id: i + 1,
     name: `Team ${i + 1}`,
     rankingPoints: Math.floor(Math.random() * 100),
     coopertition: Math.random(),
   }));
 };


 const [teams] = useState(
   generateRandomTeams().sort((a, b) =>
     b.rankingPoints === a.rankingPoints
       ? b.coopertition - a.coopertition
       : b.rankingPoints - a.rankingPoints
   ).map((team, index) => ({
     ...team,
     rank: index + 1,
   }))
 );


 const [alliances, setAlliances] = useState(
   Array.from({ length: 8 }, (_, i) => ({
     id: i + 1,
     captain: teams[i],
     members: [],
     hasPicked: false,
   }))
 );


 const [remainingTeams, setRemainingTeams] = useState(teams.slice(1));
 const [currentAllianceIndex, setCurrentAllianceIndex] = useState(0);
 const [isReverse, setIsReverse] = useState(false);
 const [error, setError] = useState('');


 const handleSelection = (teamId) => {
   setError('');
   const selectedTeam = remainingTeams.find(team => team.id === teamId);
   if (!selectedTeam) return;


   const currentAlliance = alliances[currentAllianceIndex];


   if (currentAlliance.captain.id === teamId) {
     setError('Team cannot select themselves');
     return;
   }


   if (selectedTeam.rank < currentAlliance.id) {
     setError('Alliance cannot select a higher-ranked team');
     return;
   }


   let updatedAlliances = [...alliances];
  
   updatedAlliances[currentAllianceIndex].hasPicked = true;


   const selectedCaptainIndex = alliances.findIndex(
     alliance => alliance.captain.id === selectedTeam.id
   );


   if (selectedCaptainIndex !== -1) {
     for (let i = selectedCaptainIndex; i < alliances.length - 1; i++) {
       updatedAlliances[i].captain = updatedAlliances[i + 1].captain;
       updatedAlliances[i].hasPicked = updatedAlliances[i + 1].hasPicked;
     }


     const highestRankingTeam = remainingTeams
       .filter(team =>
         team.id !== selectedTeam.id &&
         !updatedAlliances.some(a =>
           a.captain.id === team.id ||
           a.members.some(m => m.id === team.id)
         )
       )
       .sort((a, b) => a.rank - b.rank)[0];


     if (highestRankingTeam) {
       updatedAlliances[alliances.length - 1].captain = highestRankingTeam;
       updatedAlliances[alliances.length - 1].hasPicked = false;
     }
   }


   updatedAlliances[currentAllianceIndex].members.push(selectedTeam);


   setAlliances(updatedAlliances);


   const availableTeams = teams.filter(team => {
     if (team.id === selectedTeam.id) return false;
    
     if (updatedAlliances.some(alliance =>
       alliance.members.some(member => member.id === team.id)
     )) return false;
    
     const allianceAsCaptain = updatedAlliances.find(alliance =>
       alliance.captain.id === team.id
     );
     if (allianceAsCaptain && allianceAsCaptain.hasPicked) return false;
    
     return true;
   }).sort((a, b) => a.rank - b.rank);


   setRemainingTeams(availableTeams);


   const allFull = updatedAlliances.every(alliance => alliance.members.length === 2);
   if (allFull) return;


   let nextIndex = currentAllianceIndex + (isReverse ? -1 : 1);


   if (nextIndex === alliances.length || nextIndex === -1) {
     setIsReverse(prev => !prev);
     nextIndex = isReverse ? 0 : alliances.length - 1;
   }


   setCurrentAllianceIndex(nextIndex);
 };


 const totalSelected = alliances.reduce((sum, alliance) => sum + alliance.members.length, 8);


 if (totalSelected >= 24) {
   return (
     <ScrollView
       contentContainerStyle={styles.scrollContainer}
       keyboardShouldPersistTaps="handled"
     >
       <Card style={styles.container}>
         <Card.Header>
           <Card.Title>Finalized Alliances</Card.Title>
         </Card.Header>
         <Card.Content>
           <View style={styles.allianceGrid}>
             {alliances.map(alliance => (
               <Card key={alliance.id} style={styles.allianceCard}>
                 <Text style={styles.finalizedAllianceTitle}>Alliance {alliance.id}</Text>
                 <View style={styles.allianceDetails}>
                   <Text style={styles.finalizedCaptainText}>
                     Captain: {alliance.captain.name}
                     <Text style={styles.finalizedRankText}>(Rank {alliance.captain.rank})</Text>
                   </Text>
                   {alliance.members.map(member => (
                     <Text key={member.id} style={styles.finalizedMemberText}>
                       {member.name}
                       <Text style={styles.finalizedRankText}>(Rank {member.rank})</Text>
                     </Text>
                   ))}
                 </View>
               </Card>
             ))}
           </View>
         </Card.Content>
       </Card>
     </ScrollView>
   );
 }


 return (
   <ScrollView
     contentContainerStyle={styles.scrollContainer}
     keyboardShouldPersistTaps="handled"
   >
     <Card style={styles.container}>
       <Card.Header>
         <Card.Title>Alliance Selection</Card.Title>
       </Card.Header>
       <Card.Content>
         {error ? (
           <Alert variant="destructive">
             <Text style={styles.errorText}>{error}</Text>
           </Alert>
         ) : null}
        
         <View style={styles.selectionContainer}>
           <View style={styles.halfWidth}>
             <Text style={styles.sectionTitle}>Current Alliances</Text>
             <ScrollView>
               {alliances.map((alliance, index) => (
                 <Card
                   key={alliance.id}
                   style={[
                     styles.allianceCard,
                     index === currentAllianceIndex && styles.currentAlliance
                   ]}
                 >
                   <Text style={styles.allianceTitle}>Alliance {alliance.id}</Text>
                   <View style={styles.allianceDetails}>
                     <Text style={styles.captainText}>
                       Captain: {alliance.captain.name}
                       <Text style={styles.rankText}>(Rank {alliance.captain.rank})</Text>
                       {alliance.hasPicked && (
                         <Text style={styles.pickedText}> (Has Picked)</Text>
                       )}
                     </Text>
                     {alliance.members.map(member => (
                       <Text key={member.id}>
                         {member.name}
                         <Text style={styles.rankText}>(Rank {member.rank})</Text>
                       </Text>
                     ))}
                   </View>
                 </Card>
               ))}
             </ScrollView>
           </View>


           <View style={styles.halfWidth}>
             <Text style={styles.sectionTitle}>Available Teams</Text>
             <ScrollView>
               {remainingTeams.map(team => {
                 const isCaptain = alliances.some(alliance =>
                   alliance.captain.id === team.id && !alliance.hasPicked
                 );
                 return (
                   <Button
                     key={team.id}
                     onPress={() => handleSelection(team.id)}
                     disabled={team.rank === 1 || totalSelected >= 24}
                     variant={isCaptain ? "secondary" : "outline"}
                   >
                     <View style={styles.buttonContent}>
                       <Text>{team.name}</Text>
                       <Text style={styles.rankText}>
                         Rank {team.rank}
                         {isCaptain && " (Captain)"}
                       </Text>
                     </View>
                   </Button>
                 );
               })}
             </ScrollView>
           </View>
         </View>
       </Card.Content>
     </Card>
   </ScrollView>
 );
};


const styles = StyleSheet.create({
 scrollContainer: {
   flexGrow: 1,
   minHeight: Dimensions.get('window').height,
 },
 container: {
   flex: 1,
   padding: 16,
   backgroundColor: '#f5f5f5',
 },
 card: {
   backgroundColor: 'white',
   borderRadius: 8,
   shadowColor: '#000',
   shadowOffset: { width: 0, height: 2 },
   shadowOpacity: 0.1,
   shadowRadius: 4,
   elevation: 3,
 },
 cardHeader: {
   marginBottom: 16,
 },
 cardTitle: {
   fontSize: 20,
   fontWeight: 'bold',
 },
 selectionContainer: {
   flexDirection: 'row',
   justifyContent: 'space-between',
 },
 halfWidth: {
   width: '48%',
 },
 sectionTitle: {
   fontSize: 18,
   fontWeight: 'bold',
   marginBottom: 16,
 },
 allianceCard: {
   padding: 16,
   marginBottom: 12,
   borderWidth: 1,
   borderColor: '#e0e0e0',
 },
 currentAlliance: {
   borderColor: '#2196f3',
   borderWidth: 2,
 },
 allianceTitle: {
   fontSize: 16,
   fontWeight: 'bold',
   marginBottom: 8,
 },
 allianceDetails: {
   marginTop: 8,
 },
 captainText: {
   fontWeight: 'bold',
 },
 rankText: {
   color: '#666',
   fontSize: 12,
 },
 pickedText: {
   color: 'green',
 },
 button: {
   padding: 12,
   borderRadius: 8,
   marginBottom: 8,
   flexDirection: 'row',
   justifyContent: 'space-between',
   alignItems: 'center',
 },
 buttonOutline: {
   borderWidth: 1,
   borderColor: '#e0e0e0',
 },
 buttonSecondary: {
   backgroundColor: '#e0e0e0',
 },
 buttonDisabled: {
   opacity: 0.5,
 },
 buttonContent: {
   flexDirection: 'row',
   justifyContent: 'space-between',
   width: '100%',
 },
 alert: {
   padding: 16,
   borderRadius: 8,
   marginBottom: 16,
 },
 alertDestructive: {
   backgroundColor: '#ffcdd2',
   borderColor: '#f44336',
 },
 errorText: {
   color: '#d32f2f',
 },
 allianceGrid: {
   flexDirection: 'row',
   flexWrap: 'wrap',
   justifyContent: 'space-between',
 },
 // New styles for finalized screen
 finalizedAllianceTitle: {
   fontSize: 22,
   fontWeight: 'bold',
   marginBottom: 12,
   textAlign: 'center',
 },
 finalizedCaptainText: {
   fontSize: 18,
   fontWeight: 'bold',
   marginBottom: 8,
 },
 finalizedMemberText: {
   fontSize: 16,
   marginBottom: 4,
 },
 finalizedRankText: {
   fontSize: 14,
   color: '#666',
 },
});


export default AllianceSelection;