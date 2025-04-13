package com.characters.service;

import com.characters.model.GameCharacters;
import com.characters.repository.CharacterRepository;
import org.springframework.stereotype.Service;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;

import java.util.List;
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

    @Tool(name = "createCharacter", description = "Create a new character with the given details.")
    public GameCharacters createCharacter(
            @ToolParam(description = "Character details respecting the GameCharacters object fields") GameCharacters character) {
        if (character.getCharacterId() == null || character.getCharacterId().isEmpty()) {
            character.setCharacterId(UUID.randomUUID().toString());
        }
        return characterRepository.save(character);
    }

    public Optional<GameCharacters> getCharacter(String characterId) {
        return characterRepository.findById(characterId);
    }

    public List<GameCharacters> getAllCharacters() {
        return characterRepository.findAll();
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

    public void deleteCharacter(String characterId) {
        characterRepository.delete(characterId);
    }

    public List<GameCharacters> getCharactersByPlayerId(String playerId) {
        return characterRepository.findByPlayerId(playerId);
    }

    /**
     * Add experience to a character and handle level progression
     * 
     * @param characterId     The character's ID
     * @param experienceToAdd Amount of XP to add
     * @return Updated character if found, empty otherwise
     */
    @Tool(name = "addExperience", description = "Add experience to a character and handle level progression.")
    public Optional<GameCharacters> addExperience(@ToolParam(description = "ID of the character to add experience to") String characterId, @ToolParam(description = "Amount of experience to add") int experienceToAdd) {
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
    public Optional<CharacterProgressionInfo> getProgressionInfo(@ToolParam(description = "ID of the character to get progression info for") String characterId) {
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
