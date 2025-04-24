package com.characters;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.util.List;

import org.springframework.ai.tool.ToolCallback;
import org.springframework.ai.tool.ToolCallbacks;

import com.characters.service.CharacterService;

@SpringBootApplication
public class GameCharactersApplication {

    public static void main(String[] args) {
        SpringApplication.run(GameCharactersApplication.class, args);
    }

    @Bean
    public List<ToolCallback> characterTools(CharacterService gameCharacters) {
        return List.of(ToolCallbacks.from(gameCharacters));
    }
}
