package com.characters.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import software.amazon.awssdk.enhanced.dynamodb.mapper.annotations.DynamoDbBean;
import software.amazon.awssdk.enhanced.dynamodb.mapper.annotations.DynamoDbPartitionKey;
import software.amazon.awssdk.enhanced.dynamodb.mapper.annotations.DynamoDbAttribute;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@DynamoDbBean
public class GameCharacters {
    private String characterId;
    private String characterName;
    private String playerId;
    private String name;
    private String characterClass;  // "class" is a reserved keyword in Java
    private String race;
    private String gender;
    private Integer level;
    private Integer experience;
    private Stats stats;
    private List<InventoryItem> inventory;
    private CurrentStatus currentStatus;

    @DynamoDbPartitionKey
    @DynamoDbAttribute("character_id")
    public String getCharacterId() {
        return characterId;
    }
    
    public void setCharacterId(String characterId) {
        this.characterId = characterId;
    }
    
    @DynamoDbAttribute("character_name")
    public String getCharacterName() {
        return characterName;
    }
    
    public void setCharacterName(String characterName) {
        this.characterName = characterName;
    }
    
    @DynamoDbAttribute("player_id")
    public String getPlayerId() {
        return playerId;
    }
    
    public void setPlayerId(String playerId) {
        this.playerId = playerId;
    }
    
    @DynamoDbAttribute("class")
    public String getCharacterClass() {
        return characterClass;
    }
    
    public void setCharacterClass(String characterClass) {
        this.characterClass = characterClass;
    }
    
    @DynamoDbAttribute("current_status")
    public CurrentStatus getCurrentStatus() {
        return currentStatus;
    }
    
    public void setCurrentStatus(CurrentStatus currentStatus) {
        this.currentStatus = currentStatus;
    }
    
    @DynamoDbAttribute("stats")
    public Stats getStats() {
        return stats;
    }
    
    public void setStats(Stats stats) {
        this.stats = stats;
    }
}
