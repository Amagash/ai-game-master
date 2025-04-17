package com.characters;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;

import com.characters.service.CharacterService;

@SpringBootApplication
public class GameCharactersApplication {

    public static void main(String[] args) {
        SpringApplication.run(GameCharactersApplication.class, args);
    }

    @Bean
    ToolCallbackProvider gameCharactersToolCallbackProvider(
            CharacterService gameCharacters) {
        return MethodToolCallbackProvider.builder()
                .toolObjects(gameCharacters)
                .build();
    }
}
