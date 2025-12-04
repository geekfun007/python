/**
 * User Service Thrift IDL
 * 用户服务 Thrift 接口定义
 */

namespace py user_service
namespace java com.example.userservice

/**
 * 用户结构体
 */
struct User {
    1: required i32 id,
    2: required string username,
    3: required string email,
    4: optional string full_name,
    5: optional i32 age,
    6: required bool is_active,
    7: optional i64 created_at,
    8: optional i64 updated_at
}

/**
 * 用户创建请求
 */
struct UserCreateRequest {
    1: required string username,
    2: required string email,
    3: required string password,
    4: optional string full_name,
    5: optional i32 age
}

/**
 * 用户更新请求
 */
struct UserUpdateRequest {
    1: optional string full_name,
    2: optional i32 age,
    3: optional string password
}

/**
 * 用户列表响应
 */
struct UserListResponse {
    1: required i32 total,
    2: required list<User> users
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
 * 用户服务异常
 */
exception UserNotFoundException {
    1: string message
}

exception UserAlreadyExistsException {
    1: string message
}

exception ValidationException {
    1: string message,
    2: map<string, string> errors
}

/**
 * 用户服务接口
 */
service UserService {
    /**
     * 创建用户
     */
    User createUser(1: UserCreateRequest request) 
        throws (1: UserAlreadyExistsException e1, 2: ValidationException e2),
    
    /**
     * 获取用户详情
     */
    User getUser(1: i32 user_id) 
        throws (1: UserNotFoundException e),
    
    /**
     * 获取用户列表
     */
    UserListResponse listUsers(1: i32 skip, 2: i32 limit),
    
    /**
     * 更新用户
     */
    User updateUser(1: i32 user_id, 2: UserUpdateRequest request) 
        throws (1: UserNotFoundException e1, 2: ValidationException e2),
    
    /**
     * 删除用户
     */
    Response deleteUser(1: i32 user_id) 
        throws (1: UserNotFoundException e),
    
    /**
     * 搜索用户
     */
    UserListResponse searchUsers(1: string keyword, 2: i32 skip, 3: i32 limit)
}
