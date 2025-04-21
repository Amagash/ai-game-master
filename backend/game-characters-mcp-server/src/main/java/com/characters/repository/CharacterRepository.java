package com.characters.repository;

import com.characters.model.GameCharacters;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Repository;
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbEnhancedClient;
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbTable;
import software.amazon.awssdk.enhanced.dynamodb.Key;
import software.amazon.awssdk.enhanced.dynamodb.TableSchema;
import software.amazon.awssdk.enhanced.dynamodb.Expression;
import software.amazon.awssdk.enhanced.dynamodb.model.PageIterable;
import software.amazon.awssdk.enhanced.dynamodb.model.ScanEnhancedRequest;
import software.amazon.awssdk.enhanced.dynamodb.internal.AttributeValues;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.Collections;



@Repository
public class CharacterRepository {

    private final DynamoDbEnhancedClient dynamoDbEnhancedClient;
    private final DynamoDbTable<GameCharacters> charactersTable;

    public CharacterRepository(
            DynamoDbEnhancedClient dynamoDbEnhancedClient,
            @Value("${aws.dynamodb.table-name}") String tableName) {
        this.dynamoDbEnhancedClient = dynamoDbEnhancedClient;
        this.charactersTable = dynamoDbEnhancedClient.table(tableName, 
                TableSchema.fromBean(GameCharacters.class));
    }

    public GameCharacters save(GameCharacters character) {
        charactersTable.putItem(character);
        return character;
    }

    public Optional<GameCharacters> findById(String characterId) {
        Key key = Key.builder().partitionValue(characterId).build();
        return Optional.ofNullable(charactersTable.getItem(key));
    }

    public List<GameCharacters> findAll() {
        PageIterable<GameCharacters> results = charactersTable.scan();
        List<GameCharacters> characters = new ArrayList<>();
        results.items().forEach(characters::add);
        return characters;
    }

    public void delete(String characterId) {
        Key key = Key.builder().partitionValue(characterId).build();
        charactersTable.deleteItem(key);
    }
    
    public List<GameCharacters> findByPlayerId(String playerId) {
        ScanEnhancedRequest scanRequest = ScanEnhancedRequest.builder()
                .filterExpression(Expression.builder()
                        .expression("playerId = :playerId")
                        .expressionValues(Collections.singletonMap(":playerId", 
                                AttributeValues.stringValue(playerId)))
                        .build())
                .build();
                
        PageIterable<GameCharacters> results = charactersTable.scan(scanRequest);
        List<GameCharacters> characters = new ArrayList<>();
        results.items().forEach(characters::add);
        return characters;
    }
        
        
}
