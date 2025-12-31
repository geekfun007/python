/**
 * User Service Thrift IDL
 * 定义用户相关的类型和服务接口
 */

namespace py app.thrift.user

/**
 * 用户状态枚举
 */
enum UserStatus {
    INACTIVE = 0,   // 未激活
    ACTIVE = 1,     // 已激活
    BANNED = 2,     // 已封禁
    DELETED = 3     // 已删除
}

/**
 * 用户角色枚举
 */
enum UserRole {
    USER = 0,       // 普通用户
    ADMIN = 1,      // 管理员
    SUPER_ADMIN = 2 // 超级管理员
}

/**
 * 用户基础信息结构
 */
struct UserBase {
    1: required string username,
    2: required string email,
    3: optional string phone,
    4: optional string avatar,
}

/**
 * 用户创建请求
 */
struct UserCreateRequest {
    1: required string username,
    2: required string email,
    3: required string password,
    4: optional string phone,
    5: optional string avatar,
}

/**
 * 用户更新请求
 */
struct UserUpdateRequest {
    1: optional string username,
    2: optional string email,
    3: optional string phone,
    4: optional string avatar,
    5: optional UserStatus status,
    6: optional UserRole role,
}

/**
 * 用户响应结构
 */
struct UserResponse {
    1: required i64 id,
    2: required string username,
    3: required string email,
    4: optional string phone,
    5: optional string avatar,
    6: required UserStatus status,
    7: required UserRole role,
    8: required string created_at,
    9: required string updated_at,
}

/**
 * 用户列表响应
 */
struct UserListResponse {
    1: required list<UserResponse> users,
    2: required i32 total,
    3: required i32 page,
    4: required i32 page_size,
}

/**
 * 登录请求
 */
struct LoginRequest {
    1: required string email,
    2: required string password,
}

/**
 * 登录响应
 */
struct LoginResponse {
    1: required string access_token,
    2: required string token_type,
    3: required i32 expires_in,
    4: required UserResponse user,
}

/**
 * 用户服务异常
 */
exception UserNotFoundException {
    1: string message = "User not found",
}

exception UserAlreadyExistsException {
    1: string message = "User already exists",
}

exception InvalidCredentialsException {
    1: string message = "Invalid credentials",
}

/**
 * 用户服务接口定义
 */
service UserService {
    // 创建用户
    UserResponse createUser(1: UserCreateRequest request) 
        throws (1: UserAlreadyExistsException ex),
    
    // 获取用户
    UserResponse getUser(1: i64 user_id) 
        throws (1: UserNotFoundException ex),
    
    // 获取用户列表
    UserListResponse listUsers(1: i32 page, 2: i32 page_size),
    
    // 更新用户
    UserResponse updateUser(1: i64 user_id, 2: UserUpdateRequest request) 
        throws (1: UserNotFoundException ex),
    
    // 删除用户
    bool deleteUser(1: i64 user_id) 
        throws (1: UserNotFoundException ex),
    
    // 用户登录
    LoginResponse login(1: LoginRequest request) 
        throws (1: InvalidCredentialsException ex),
}
