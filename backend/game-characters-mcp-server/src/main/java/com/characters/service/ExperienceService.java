package com.characters.service;

import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

/**
 * Service to handle D&D 5e experience and leveling mechanics
 * Based on the D&D 2018 Basic Rules
 */
@Service
public class ExperienceService {

    // Experience thresholds for each level according to D&D 5e Basic Rules
    private static final Map<Integer, Integer> LEVEL_THRESHOLDS = new HashMap<>();
    
    static {
        LEVEL_THRESHOLDS.put(1, 0);
        LEVEL_THRESHOLDS.put(2, 300);
        LEVEL_THRESHOLDS.put(3, 900);
        LEVEL_THRESHOLDS.put(4, 2700);
        LEVEL_THRESHOLDS.put(5, 6500);
        LEVEL_THRESHOLDS.put(6, 14000);
        LEVEL_THRESHOLDS.put(7, 23000);
        LEVEL_THRESHOLDS.put(8, 34000);
        LEVEL_THRESHOLDS.put(9, 48000);
        LEVEL_THRESHOLDS.put(10, 64000);
        LEVEL_THRESHOLDS.put(11, 85000);
        LEVEL_THRESHOLDS.put(12, 100000);
        LEVEL_THRESHOLDS.put(13, 120000);
        LEVEL_THRESHOLDS.put(14, 140000);
        LEVEL_THRESHOLDS.put(15, 165000);
        LEVEL_THRESHOLDS.put(16, 195000);
        LEVEL_THRESHOLDS.put(17, 225000);
        LEVEL_THRESHOLDS.put(18, 265000);
        LEVEL_THRESHOLDS.put(19, 305000);
        LEVEL_THRESHOLDS.put(20, 355000);
    }
    
    /**
     * Calculate the level based on total experience points
     * 
     * @param experiencePoints Total XP of the character
     * @return The character's level based on XP
     */
    public int calculateLevel(int experiencePoints) {
        int level = 1;
        
        for (int i = 20; i > 0; i--) {
            if (experiencePoints >= LEVEL_THRESHOLDS.get(i)) {
                level = i;
                break;
            }
        }
        
        return level;
    }
    
    /**
     * Check if a character has leveled up after gaining experience
     * 
     * @param currentLevel Current character level
     * @param totalExperience Total experience after gaining new XP
     * @return true if the character leveled up, false otherwise
     */
    public boolean hasLeveledUp(int currentLevel, int totalExperience) {
        int newLevel = calculateLevel(totalExperience);
        return newLevel > currentLevel;
    }
    
    /**
     * Get the experience needed for the next level
     * 
     * @param currentLevel Current character level
     * @return XP needed for next level, or 0 if already at max level
     */
    public int experienceForNextLevel(int currentLevel) {
        if (currentLevel >= 20) {
            return 0; // Already at max level
        }
        
        return LEVEL_THRESHOLDS.get(currentLevel + 1) - LEVEL_THRESHOLDS.get(currentLevel);
    }
    
    /**
     * Get the total experience needed to reach a specific level
     * 
     * @param targetLevel The level to reach
     * @return Total XP needed for that level
     */
    public int experienceForLevel(int targetLevel) {
        if (targetLevel < 1) {
            return 0;
        }
        
        if (targetLevel > 20) {
            targetLevel = 20;
        }
        
        return LEVEL_THRESHOLDS.get(targetLevel);
    }
}
