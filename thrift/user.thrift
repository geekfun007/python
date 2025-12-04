/**
 * User Service Thrift Definition
 * 用户服务 Thrift 定义
 */

namespace py user_service
namespace java com.example.user

/**
 * 用户信息
 */
struct User {
    1: required i32 id,
    2: required string username,
    3: required string email,
    4: optional string full_name,
    5: optional i32 age,
    6: required bool is_active,
    7: required bool is_superuser,
    8: required string created_at,
    9: required string updated_at
}

/**
 * 创建用户请求
 */
struct CreateUserRequest {
    1: required string username,
    2: required string email,
    3: required string password,
    4: optional string full_name,
    5: optional i32 age
}

/**
 * 更新用户请求
 */
struct UpdateUserRequest {
    1: optional string full_name,
    2: optional i32 age,
    3: optional bool is_active
}

/**
 * 用户列表响应
 */
struct UserListResponse {
    1: required i32 total,
    2: required list<User> items
}

/**
 * 通用响应
 */
struct Response {
    1: required i32 code,
    2: required string message,
    3: optional string data
}

/**
 * 异常定义
 */
exception UserNotFoundException {
    1: string message
}

exception UserAlreadyExistsException {
    1: string message
}

exception ValidationException {
    1: string message
}

/**
 * 用户服务接口
 */
service UserService {
    /**
     * 创建用户
     */
    User createUser(1: CreateUserRequest request) 
        throws (1: UserAlreadyExistsException uaee, 2: ValidationException ve),
    
    /**
     * 获取用户
     */
    User getUser(1: i32 user_id) 
        throws (1: UserNotFoundException unfe),
    
    /**
     * 获取用户列表
     */
    UserListResponse getUserList(1: i32 skip, 2: i32 limit),
    
    /**
     * 更新用户
     */
    User updateUser(1: i32 user_id, 2: UpdateUserRequest request) 
        throws (1: UserNotFoundException unfe, 2: ValidationException ve),
    
    /**
     * 删除用户
     */
    Response deleteUser(1: i32 user_id) 
        throws (1: UserNotFoundException unfe),
    
    /**
     * 搜索用户
     */
    UserListResponse searchUsers(1: string search_term, 2: i32 skip, 3: i32 limit)
}
