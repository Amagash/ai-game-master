package com.characters.service;

import com.characters.model.GameCharacters;
import com.characters.model.InventoryItem;
import com.characters.model.CurrentStatus;
import com.characters.model.Stats;
import com.characters.repository.CharacterRepository;

import com.characters.service.ExperienceService;
import org.springframework.stereotype.Service;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

@Service
public class CharacterService {

    private final CharacterRepository characterRepository;
    private final ExperienceService experienceService;

    public CharacterService(CharacterRepository characterRepository, ExperienceService experienceService) {
        this.characterRepository = characterRepository;
        this.experienceService = experienceService;
    }

    private void defaultConfig4Character(GameCharacters character) {
        // Validate and set default values for essential character fields
        if (character.getPlayerId() == null || character.getPlayerId().isEmpty()) {
            throw new IllegalArgumentException("Player ID is required");
        }
        if (character.getName() == null || character.getName().isEmpty()) {
            throw new IllegalArgumentException("Character name is required");
        }

        // Set default values if not present
        if (character.getLevel() == null || character.getLevel() == 0) {
            character.setLevel(1); // Default starting level
        }
        if (character.getExperience() == null || character.getExperience() == 0) {
            character.setExperience(0); // Default starting XP
        }

        // Set default stats if not present
        if (character.getStats() == null) {
            Stats stats = Stats.builder()
                    .strength(10)
                    .dexterity(10)
                    .constitution(10)
                    .intelligence(10)
                    .wisdom(10)
                    .charisma(10)
                    .build();
            character.setStats(stats);
        }

        // Calculate and set default HP based on class and constitution
        if (character.getCurrentStatus() == null) {
            CurrentStatus status = new CurrentStatus();
            int baseHp = getBaseHpForClass(character.getCharacterClass());
            int constitutionModifier = (character.getStats().getConstitution() - 10) / 2;
            int maxHp = baseHp + constitutionModifier;

            status.setMaxHp(maxHp);
            status.setHp(maxHp);
            status.setCondition("Normal");
            status.setBuffs(new ArrayList<>());
            character.setCurrentStatus(status);
        }

        // Set default inventory if not present
        if (character.getInventory() == null || character.getInventory().isEmpty()) {
            character.setInventory(createDefaultInventory());
        }
    }

    private int getBaseHpForClass(String characterClass) {
        Map<String, Integer> baseHpMap = new HashMap<>();
        baseHpMap.put("Barbarian", 12);
        baseHpMap.put("Fighter", 10);
        baseHpMap.put("Paladin", 10);
        baseHpMap.put("Ranger", 10);
        baseHpMap.put("Bard", 8);
        baseHpMap.put("Cleric", 8);
        baseHpMap.put("Druid", 8);
        baseHpMap.put("Monk", 8);
        baseHpMap.put("Rogue", 8);
        baseHpMap.put("Warlock", 8);
        baseHpMap.put("Sorcerer", 6);
        baseHpMap.put("Wizard", 6);

        return baseHpMap.getOrDefault(characterClass, 8);
    }

    private List<InventoryItem> createDefaultInventory() {
        List<InventoryItem> defaultInventory = new ArrayList<>();
        defaultInventory.add(new InventoryItem("Shortsword", 1));
        defaultInventory.add(new InventoryItem("Shortbow", 1));
        defaultInventory.add(new InventoryItem("Arrows", 20));
        defaultInventory.add(new InventoryItem("Leather Armor", 1));
        defaultInventory.add(new InventoryItem("Torch", 2));
        defaultInventory.add(new InventoryItem("Flint & Tinder", 1));
        defaultInventory.add(new InventoryItem("Rations", 5));
        defaultInventory.add(new InventoryItem("Waterskin", 1));
        defaultInventory.add(new InventoryItem("Map or Blank Parchment", 1));
        defaultInventory.add(new InventoryItem("Quill & Ink", 1));
        defaultInventory.add(new InventoryItem("Health Potion", 1));
        defaultInventory.add(new InventoryItem("Gold Pieces", 10));

        return defaultInventory;
    }

    @Tool(name = "createCharacter", description = "Create a new character with the given details.")
    public GameCharacters createCharacter(
            @ToolParam(description = "Character details respecting the GameCharacters object fields") GameCharacters character) {
        if (character == null) {
            throw new IllegalArgumentException("Character cannot be null");
        }
        // Check for character ID and generate if missing
        if (character.getCharacterId() == null || character.getCharacterId().isEmpty()) {
            character.setCharacterId(UUID.randomUUID().toString());
        }

        defaultConfig4Character(character);

        return characterRepository.save(character);
    }

    @Tool(name = "updateCharacter", description = "Update an existing character's details.")
    public Optional<GameCharacters> updateCharacter(
            @ToolParam(description = "ID of the character to update") String characterId,
            @ToolParam(description = "Updated character details respecting the GameCharacters object fields") GameCharacters updatedCharacter) {
        Optional<GameCharacters> existingCharacter = characterRepository.findById(characterId);

        if (existingCharacter.isPresent()) {
            updatedCharacter.setCharacterId(characterId);
            return Optional.of(characterRepository.save(updatedCharacter));
        }

        return Optional.empty();
    }

    @Tool(name = "getCharacter", description = "Retrieve a character by their ID from the database")
    public GameCharacters getCharacter(
            @ToolParam(description = "ID of the character to retrieve") String characterId) {
        // Validate input
        if (characterId == null || characterId.isEmpty()) {
            throw new IllegalArgumentException("Character ID cannot be null or empty");
        }

        // Attempt to retrieve character
        Optional<GameCharacters> character = characterRepository.findById(characterId);

        // Throw exception if character not found
        if (!character.isPresent()) {
            throw new RuntimeException("Character not found with ID: " + characterId);
        }

        return character.get();
    }

    @Tool(name = "getCharactersByPlayerId", description = "Retrieve all characters belonging to a specific player")
    public List<GameCharacters> getCharactersByPlayerId(
            @ToolParam(description = "ID of the player to retrieve characters for") String playerId) {
        // Validate input
        if (playerId == null || playerId.isEmpty()) {
            throw new IllegalArgumentException("Player ID cannot be null or empty");
        }

        // Check if any characters exist for this player ID
        List<GameCharacters> characters = characterRepository.findByPlayerId(playerId);

        if (characters.isEmpty()) {
            throw new RuntimeException("No characters found for player ID: " + playerId);
        }

        return characters;
    }

    /**
     * Add experience to a character and handle level progression
     * 
     * @param characterId     The character's ID
     * @param experienceToAdd Amount of XP to add
     * @return Updated character if found, empty otherwise
     */
    @Tool(name = "addExperience", description = "Add experience to a character and handle level progression.")
    public Optional<GameCharacters> addExperience(
            @ToolParam(description = "ID of the character to add experience to") String characterId,
            @ToolParam(description = "Amount of experience to add") int experienceToAdd) {
        Optional<GameCharacters> characterOpt = characterRepository.findById(characterId);

        if (characterOpt.isPresent()) {
            GameCharacters character = characterOpt.get();
            int currentLevel = character.getLevel();
            int currentExp = character.getExperience();
            int newTotalExp = currentExp + experienceToAdd;

            // Update experience
            character.setExperience(newTotalExp);

            // Check if character leveled up
            int newLevel = experienceService.calculateLevel(newTotalExp);
            if (newLevel > currentLevel) {
                character.setLevel(newLevel);
                // Level up logic could be expanded here (e.g., increase HP, etc.)
            }

            // Save and return updated character
            return Optional.of(characterRepository.save(character));
        }

        return Optional.empty();
    }

    /**
     * Get information about a character's progression
     * 
     * @param characterId The character's ID
     * @return Map containing progression details or empty if character not found
     */
    @Tool(name = "getProgressionInfo", description = "Get information about a character's progression during a Game Session.")
    public Optional<CharacterProgressionInfo> getProgressionInfo(
            @ToolParam(description = "ID of the character to get progression info for") String characterId) {
        Optional<GameCharacters> characterOpt = characterRepository.findById(characterId);

        if (characterOpt.isPresent()) {
            GameCharacters character = characterOpt.get();
            int currentLevel = character.getLevel();
            int currentExp = character.getExperience();

            CharacterProgressionInfo progressInfo = new CharacterProgressionInfo();
            progressInfo.setCurrentLevel(currentLevel);
            progressInfo.setCurrentExperience(currentExp);
            progressInfo.setExperienceForCurrentLevel(experienceService.experienceForLevel(currentLevel));

            if (currentLevel < 20) {
                progressInfo.setExperienceForNextLevel(experienceService.experienceForLevel(currentLevel + 1));
                progressInfo.setExperienceNeeded(progressInfo.getExperienceForNextLevel() - currentExp);
            } else {
                progressInfo.setExperienceForNextLevel(0);
                progressInfo.setExperienceNeeded(0);
            }

            return Optional.of(progressInfo);
        }

        return Optional.empty();
    }

    /**
     * Class to hold character progression information
     */
    public static class CharacterProgressionInfo {
        private int currentLevel;
        private int currentExperience;
        private int experienceForCurrentLevel;
        private int experienceForNextLevel;
        private int experienceNeeded;

        // Getters and setters
        public int getCurrentLevel() {
            return currentLevel;
        }

        public void setCurrentLevel(int currentLevel) {
            this.currentLevel = currentLevel;
        }

        public int getCurrentExperience() {
            return currentExperience;
        }

        public void setCurrentExperience(int currentExperience) {
            this.currentExperience = currentExperience;
        }

        public int getExperienceForCurrentLevel() {
            return experienceForCurrentLevel;
        }

        public void setExperienceForCurrentLevel(int experienceForCurrentLevel) {
            this.experienceForCurrentLevel = experienceForCurrentLevel;
        }

        public int getExperienceForNextLevel() {
            return experienceForNextLevel;
        }

        public void setExperienceForNextLevel(int experienceForNextLevel) {
            this.experienceForNextLevel = experienceForNextLevel;
        }

        public int getExperienceNeeded() {
            return experienceNeeded;
        }

        public void setExperienceNeeded(int experienceNeeded) {
            this.experienceNeeded = experienceNeeded;
        }
    }
}
