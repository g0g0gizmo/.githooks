---
description: 'JUnit 5 testing framework best practices for Java and Spring Boot applications'
applyTo: '**/*Test.java,**/*Tests.java'
---

## Core Engineering Principles

This instruction set applies the following foundational principles:

- [DRY (Don't Repeat Yourself)](../core/principles/dont-repeat-yourself.md) - Use shared fixtures and test utilities to minimize duplication
- [Code Quality Goals](../core/principles/code-quality-goals.md) - Maintain clear assertions and comprehensive test coverage
- [Testing Standards](../core/principles/testing-standards.md) - Follow AAA pattern and organize tests by behavior

When writing JUnit 5 tests, always consider how they reinforce these core principles and create maintainable test suites.

---

# JUnit 5 + Java Testing

## Overview

JUnit 5 (Jupiter) is the latest evolution of the popular Java testing framework. It provides modern features including parametrized tests, dynamic tests, extensions, and seamless integration with Spring Boot, Mockito, and other testing libraries.

## JUnit 5 Setup and Configuration

### Maven Dependencies
```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.9.3</version>
    <scope>test</scope>
</dependency>

<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-core</artifactId>
    <version>5.3.1</version>
    <scope>test</scope>
</dependency>

<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-junit-jupiter</artifactId>
    <version>5.3.1</version>
    <scope>test</scope>
</dependency>

<dependency>
    <groupId>org.assertj</groupId>
    <artifactId>assertj-core</artifactId>
    <version>3.24.1</version>
    <scope>test</scope>
</dependency>
```

### Gradle Dependencies
```gradle
testImplementation 'org.junit.jupiter:junit-jupiter:5.9.3'
testImplementation 'org.mockito:mockito-core:5.3.1'
testImplementation 'org.mockito:mockito-junit-jupiter:5.3.1'
testImplementation 'org.assertj:assertj-core:3.24.1'
```

### junit-platform.properties Configuration
```properties
# Display names for parametrized tests
junit.jupiter.params.display.name.pattern = {index} -> {arguments}

# Display names for dynamic tests
junit.jupiter.dynamic.test.name.pattern = {index} -> {displayName}

# Execution behavior
junit.jupiter.execution.parallel.enabled = true
junit.jupiter.execution.parallel.mode.default = concurrent
junit.jupiter.execution.parallel.mode.classes.default = concurrent
```

## Test File Organization

### Directory Structure
```
src/
├── main/
│   ├── java/
│   │   └── com/example/
│   │       ├── services/
│   │       │   ├── UserService.java
│   │       │   └── PaymentService.java
│   │       ├── models/
│   │       │   └── User.java
│   │       └── utils/
│   │           └── Helpers.java
│   └── resources/
│       └── application.properties
└── test/
    ├── java/
    │   └── com/example/
    │       ├── services/
    │       │   ├── UserServiceTest.java
    │       │   └── PaymentServiceTest.java
    │       ├── utils/
    │       │   └── HelpersTest.java
    │       └── fixtures/
    │           ├── DatabaseFixture.java
    │           └── TestDataBuilder.java
    └── resources/
        └── application-test.properties
```

### Naming Convention
- Test classes: `[Class]Test` or `[Class]Tests`
- Test methods: `[method]_[scenario]_[expected]`
  - Example: `login_withValidCredentials_returnsAuthToken`
  - Alternative: `shouldReturnAuthTokenWhenLoginWithValidCredentials`
- Fixtures: `[Resource]Fixture`

## Test Structure (AAA Pattern)

All tests must follow **Arrange-Act-Assert** pattern:

```java
public class UserServiceTest {

    private UserService userService;
    private UserRepository userRepository;

    @BeforeEach
    void setUp() {
        userRepository = mock(UserRepository.class);
        userService = new UserService(userRepository);
    }

    @Test
    void createUser_withValidInput_returnsUserWithId() {
        // Arrange: Set up test data and dependencies
        CreateUserRequest request = new CreateUserRequest(
            "John Doe",
            "john@example.com"
        );

        // Act: Execute the code under test
        User result = userService.createUser(request);

        // Assert: Verify the expected outcome
        assertThat(result)
            .isNotNull()
            .extracting(User::getName, User::getEmail)
            .containsExactly("John Doe", "john@example.com");

        assertThat(result.getId()).isNotNull();
    }

    @Test
    void createUser_withInvalidEmail_throwsValidationException() {
        // Arrange
        CreateUserRequest request = new CreateUserRequest(
            "John",
            "invalid-email"
        );

        // Act & Assert
        assertThatThrownBy(() -> userService.createUser(request))
            .isInstanceOf(ValidationException.class)
            .hasMessageContaining("Invalid email");
    }
}
```

## Lifecycle Methods and Fixtures

### Setup and Teardown
```java
public class LifecycleTest {

    @BeforeAll
    static void setUpAll() {
        // Runs once before all tests in the class
        // Must be static
        System.out.println("Setting up test class");
    }

    @BeforeEach
    void setUp() {
        // Runs before each test method
        System.out.println("Setting up for individual test");
    }

    @AfterEach
    void tearDown() {
        // Runs after each test method
        System.out.println("Cleaning up after test");
    }

    @AfterAll
    static void tearDownAll() {
        // Runs once after all tests in the class
        // Must be static
        System.out.println("Cleaning up test class");
    }

    @Test
    void testExample() {
        // Test logic
    }
}
```

### Test Fixtures with Annotations
```java
public class DatabaseFixture {
    private TestDatabase testDatabase;

    @BeforeEach
    void setupDatabase() {
        testDatabase = new TestDatabase();
        testDatabase.connect();
        testDatabase.createSchema();
    }

    @AfterEach
    void cleanupDatabase() {
        testDatabase.clearData();
        testDatabase.disconnect();
    }

    protected TestDatabase getDatabase() {
        return testDatabase;
    }
}

public class UserServiceIntegrationTest extends DatabaseFixture {

    @Test
    void getUser_withExistingId_returnsUser() {
        TestDatabase db = getDatabase();
        User user = db.insertUser("John", "john@example.com");

        UserService service = new UserService(db.getRepository());
        Optional<User> found = service.getUserById(user.getId());

        assertThat(found).isPresent().contains(user);
    }
}
```

## Parameterized Tests

### @ParameterizedTest with @ValueSource
```java
public class EmailValidationTest {

    @ParameterizedTest
    @ValueSource(strings = {
        "user@example.com",
        "test.user@domain.co.uk",
        "admin+tag@example.org"
    })
    void validEmail_returnsTrue(String email) {
        assertThat(EmailValidator.isValid(email)).isTrue();
    }

    @ParameterizedTest
    @ValueSource(strings = {
        "invalid.email",
        "user@",
        "user@domain",
        ""
    })
    void invalidEmail_returnsFalse(String email) {
        assertThat(EmailValidator.isValid(email)).isFalse();
    }
}
```

### @ParameterizedTest with @CsvSource
```java
public class MathOperationTest {

    @ParameterizedTest(name = "{index} -> {0} {1} {2}")
    @CsvSource({
        "10, square, 100",
        "5, double, 10",
        "0, square, 0",
        "-5, double, -10"
    })
    void performOperation_withVariousInputs_returnsExpected(
            int input, String operation, int expected) {
        int result = MathHelper.perform(input, operation);
        assertThat(result).isEqualTo(expected);
    }
}
```

### @ParameterizedTest with @MethodSource
```java
public class UserValidationTest {

    static Stream<Arguments> provideUsers() {
        return Stream.of(
            Arguments.of(
                new CreateUserRequest("John", "john@example.com"),
                true
            ),
            Arguments.of(
                new CreateUserRequest("", "test@example.com"),
                false
            ),
            Arguments.of(
                new CreateUserRequest("Jane", "invalid-email"),
                false
            )
        );
    }

    @ParameterizedTest
    @MethodSource("provideUsers")
    void validateUser_withVariousRequests_returnsExpected(
            CreateUserRequest request, boolean expected) {
        boolean result = new UserValidator().isValid(request);
        assertThat(result).isEqualTo(expected);
    }
}
```

### @ParameterizedTest with @CsvFileSource
```java
public class DataImportTest {

    @ParameterizedTest
    @CsvFileSource(resources = "/test-data.csv", numLinesToSkip = 1)
    void importData_withCsvFile_loadsCorrectly(String id, String name, int age) {
        User user = new User(id, name, age);
        assertThat(user.getName()).isEqualTo(name);
    }
}

// test-data.csv
// id,name,age
// 1,John,30
// 2,Jane,25
```

## Dynamic Tests

```java
public class DynamicTestExample {

    @TestFactory
    Collection<DynamicTest> dynamicTests() {
        List<DynamicTest> tests = new ArrayList<>();

        for (int i = 0; i < 5; i++) {
            final int number = i;
            tests.add(
                dynamicTest(
                    "Test for number " + number,
                    () -> assertThat(number).isGreaterThanOrEqualTo(0)
                )
            );
        }

        return tests;
    }

    @TestFactory
    Stream<DynamicTest> dynamicTestsFromStream() {
        return IntStream.range(0, 5)
            .mapToObj(i ->
                dynamicTest(
                    "Fibonacci: " + i,
                    () -> assertThat(fibonacci(i)).isGreaterThanOrEqualTo(0)
                )
            );
    }

    private int fibonacci(int n) {
        if (n <= 1) return n;
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}
```

## Mocking with Mockito

### Basic Mocking
```java
public class UserServiceTest {

    @Mock
    private UserRepository mockRepository;

    @InjectMocks
    private UserService userService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void getUser_withValidId_returnsUser() {
        // Arrange
        User expectedUser = new User(1L, "John", "john@example.com");
        when(mockRepository.findById(1L))
            .thenReturn(Optional.of(expectedUser));

        // Act
        Optional<User> result = userService.getUser(1L);

        // Assert
        assertThat(result)
            .isPresent()
            .contains(expectedUser);

        verify(mockRepository).findById(1L);
    }
}
```

### Advanced Mocking Patterns
```java
// Argument Matchers
when(mockRepository.findByEmail(any(String.class)))
    .thenReturn(Optional.empty());

when(mockRepository.findByEmail(argThat(email -> email.contains("@"))))
    .thenReturn(Optional.of(validUser));

// Multiple Return Values
when(mockRepository.count())
    .thenReturn(0L)
    .thenReturn(1L)
    .thenReturn(2L);

// Throw Exception
when(mockRepository.findById(-1L))
    .thenThrow(new IllegalArgumentException("Invalid ID"));

// Callback/Answer
when(mockRepository.save(any(User.class)))
    .thenAnswer(invocation -> {
        User user = invocation.getArgument(0);
        user.setId(System.currentTimeMillis());
        return user;
    });

// Void Methods
doNothing().when(mockRepository).delete(any(User.class));
doThrow(new RuntimeException()).when(mockRepository).delete(null);
```

### Verification
```java
// Verify was called
verify(mockRepository).save(any(User.class));

// Verify exact number of times
verify(mockRepository, times(2)).findById(1L);
verify(mockRepository, never()).delete(any());

// Verify call order
InOrder inOrder = inOrder(mockRepository, mockService);
inOrder.verify(mockRepository).save(user);
inOrder.verify(mockService).notifyUser(user);

// Verify no more interactions
verifyNoMoreInteractions(mockRepository, mockService);
```

## AssertJ Fluent Assertions

### Object Assertions
```java
@Test
void user_withValidData_satisfiesConditions() {
    User user = new User(1L, "John", "john@example.com");

    assertThat(user)
        .isNotNull()
        .hasFieldOrPropertyWithValue("name", "John")
        .hasFieldOrPropertyWithValue("email", "john@example.com");

    assertThat(user.getName())
        .isNotEmpty()
        .startsWith("J")
        .hasLength(4);
}
```

### Collection Assertions
```java
@Test
void getActiveUsers_returnsExpectedUsers() {
    List<User> users = Arrays.asList(
        new User(1L, "John", true),
        new User(2L, "Jane", true),
        new User(3L, "Bob", false)
    );

    List<User> activeUsers = users.stream()
        .filter(User::isActive)
        .collect(Collectors.toList());

    assertThat(activeUsers)
        .hasSize(2)
        .allSatisfy(u -> assertThat(u.isActive()).isTrue())
        .contains(users.get(0), users.get(1))
        .doesNotContain(users.get(2))
        .extracting(User::getName)
        .containsExactly("John", "Jane");
}
```

### Exception Assertions
```java
@Test
void createUser_withInvalidEmail_throwsException() {
    CreateUserRequest request = new CreateUserRequest("John", "invalid");

    assertThatThrownBy(() -> new UserValidator().validate(request))
        .isInstanceOf(ValidationException.class)
        .hasMessageContaining("Invalid email")
        .hasNoCause();
}

@Test
void operation_withEdgeCase_completesSuccessfully() {
    assertThatCode(() -> riskyOperation(null))
        .doesNotThrowAnyException();
}
```

## Test Data Builders

### Builder Pattern
```java
public class UserBuilder {
    private Long id;
    private String name = "Test User";
    private String email = "test@example.com";
    private boolean active = true;
    private LocalDateTime createdAt = LocalDateTime.now();

    public UserBuilder withName(String name) {
        this.name = name;
        return this;
    }

    public UserBuilder withEmail(String email) {
        this.email = email;
        return this;
    }

    public UserBuilder inactive() {
        this.active = false;
        return this;
    }

    public User build() {
        User user = new User();
        user.setId(id);
        user.setName(name);
        user.setEmail(email);
        user.setActive(active);
        user.setCreatedAt(createdAt);
        return user;
    }
}

// Usage
User standardUser = new UserBuilder().build();
User adminUser = new UserBuilder()
    .withName("Admin")
    .withEmail("admin@example.com")
    .build();
User inactiveUser = new UserBuilder().inactive().build();
```

## Spring Boot Testing

### @SpringBootTest
```java
@SpringBootTest
class UserServiceIntegrationTest {

    @Autowired
    private UserService userService;

    @Autowired
    private UserRepository userRepository;

    @BeforeEach
    void setUp() {
        userRepository.deleteAll();
    }

    @Test
    void createUser_withValidData_persistsToDatabase() {
        User user = userService.createUser(
            new CreateUserRequest("John", "john@example.com")
        );

        User retrieved = userRepository.findById(user.getId()).orElseThrow();
        assertThat(retrieved).isEqualTo(user);
    }
}
```

### @WebMvcTest for Controllers
```java
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Test
    void getUser_withValidId_returns200AndUser() throws Exception {
        User expectedUser = new User(1L, "John", "john@example.com");
        when(userService.getUser(1L))
            .thenReturn(Optional.of(expectedUser));

        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("John"))
            .andExpect(jsonPath("$.email").value("john@example.com"));
    }
}
```

### @DataJpaTest for Repository
```java
@DataJpaTest
class UserRepositoryTest {

    @Autowired
    private UserRepository userRepository;

    @Test
    void findByEmail_withExistingEmail_returnsUser() {
        User user = new User(null, "John", "john@example.com", true);
        userRepository.save(user);

        Optional<User> found = userRepository.findByEmail("john@example.com");

        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("John");
    }
}
```

## Best Practices

### ✓ Good Patterns

**1. Descriptive Test Names**
```java
@Test
void shouldThrowValidationExceptionWhenEmailFormatIsInvalid() {
    // Clear intent
}
```

**2. One Logical Assertion per Test**
```java
@Test
void user_withValidAge_isConsideredAdult() {
    User user = new User("John", 25);
    assertThat(user.isAdult()).isTrue();
}
```

**3. Using Builders for Complex Objects**
```java
User complexUser = new UserBuilder()
    .withName("Admin")
    .withEmail("admin@example.com")
    .build();
```

**4. Clear Arrange-Act-Assert**
```java
// Obvious separation with comments or blank lines
// Arrange
// Act
// Assert
```

### ✗ Anti-Patterns to Avoid

**1. Testing Implementation Details**
```java
// ✗ Bad: Testing private method
private int calculateAge() { ... }
assertThat(user.calculateAge()).isEqualTo(30);

// ✓ Good: Test observable behavior
assertThat(user.isAdult()).isTrue();
```

**2. Tests Dependent on Order**
```java
// ✗ Bad: Tests must run in specific order
@Test
void step1_createUser() { }

@Test
void step2_updateUser() { } // Depends on step 1
```

**3. Over-Mocking**
```java
// ✗ Bad: Unnecessary mock
Mock<String> mockString = mock(String.class);

// ✓ Good: Real simple objects
String realString = "test";
```

## Running Tests

### Command Line
```bash
# Run all tests
mvn test

# Run specific test class
mvn test -Dtest=UserServiceTest

# Run specific test method
mvn test -Dtest=UserServiceTest#createUser_withValidInput_returnsUserWithId

# Run with coverage
mvn test jacoco:report

# Run in parallel
mvn test -DthreadCount=4
```

### IDE Integration
- Run from IDE's test runner (right-click on test class or method)
- Debug with breakpoints (Shift+F9 or Debug)
- View coverage (Run → Run with Coverage)

## Code Coverage

### JaCoCo Configuration (Maven)
```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.10</version>
    <executions>
        <execution>
            <goals>
                <goal>prepare-agent</goal>
            </goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals>
                <goal>report</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

### Coverage Standards
- **Line Coverage**: Minimum 75%, target 85%+
- **Branch Coverage**: Minimum 70%, target 80%+
- **Method Coverage**: Minimum 80%, target 90%+

---

## Related Instructions

- [Java Development Guidelines](./java.instructions.md)
- [Spring Boot Best Practices](./springboot.instructions.md)
