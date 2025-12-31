/**
 * Article Service Thrift IDL
 * 定义文章相关的类型和服务接口
 */

namespace py app.thrift.article

include "user.thrift"

/**
 * 文章状态枚举
 */
enum ArticleStatus {
    DRAFT = 0,      // 草稿
    PUBLISHED = 1,  // 已发布
    ARCHIVED = 2,   // 已归档
    DELETED = 3     // 已删除
}

/**
 * 文章分类结构
 */
struct Category {
    1: required i64 id,
    2: required string name,
    3: optional string description,
    4: optional i64 parent_id,
}

/**
 * 文章标签结构
 */
struct Tag {
    1: required i64 id,
    2: required string name,
    3: optional string color,
}

/**
 * 文章创建请求
 */
struct ArticleCreateRequest {
    1: required string title,
    2: required string content,
    3: optional string summary,
    4: optional string cover_image,
    5: optional i64 category_id,
    6: optional list<i64> tag_ids,
    7: optional ArticleStatus status = ArticleStatus.DRAFT,
}

/**
 * 文章更新请求
 */
struct ArticleUpdateRequest {
    1: optional string title,
    2: optional string content,
    3: optional string summary,
    4: optional string cover_image,
    5: optional i64 category_id,
    6: optional list<i64> tag_ids,
    7: optional ArticleStatus status,
}

/**
 * 文章响应结构
 */
struct ArticleResponse {
    1: required i64 id,
    2: required string title,
    3: required string content,
    4: optional string summary,
    5: optional string cover_image,
    6: required ArticleStatus status,
    7: required i64 author_id,
    8: optional string author_name,
    9: optional Category category,
    10: optional list<Tag> tags,
    11: required i32 view_count,
    12: required i32 like_count,
    13: required i32 comment_count,
    14: required string created_at,
    15: required string updated_at,
    16: optional string published_at,
}

/**
 * 文章列表响应
 */
struct ArticleListResponse {
    1: required list<ArticleResponse> articles,
    2: required i32 total,
    3: required i32 page,
    4: required i32 page_size,
}

/**
 * 文章查询过滤器
 */
struct ArticleFilter {
    1: optional string keyword,
    2: optional i64 author_id,
    3: optional i64 category_id,
    4: optional list<i64> tag_ids,
    5: optional ArticleStatus status,
    6: optional string start_date,
    7: optional string end_date,
}

/**
 * 评论结构
 */
struct Comment {
    1: required i64 id,
    2: required i64 article_id,
    3: required i64 user_id,
    4: optional string user_name,
    5: required string content,
    6: optional i64 parent_id,
    7: required string created_at,
}

/**
 * 评论创建请求
 */
struct CommentCreateRequest {
    1: required i64 article_id,
    2: required string content,
    3: optional i64 parent_id,
}

/**
 * 服务异常
 */
exception ArticleNotFoundException {
    1: string message = "Article not found",
}

exception CategoryNotFoundException {
    1: string message = "Category not found",
}

exception UnauthorizedException {
    1: string message = "Unauthorized operation",
}

/**
 * 文章服务接口定义
 */
service ArticleService {
    // 创建文章
    ArticleResponse createArticle(1: i64 author_id, 2: ArticleCreateRequest request),
    
    // 获取文章
    ArticleResponse getArticle(1: i64 article_id) 
        throws (1: ArticleNotFoundException ex),
    
    // 获取文章列表
    ArticleListResponse listArticles(1: i32 page, 2: i32 page_size, 3: ArticleFilter filter),
    
    // 更新文章
    ArticleResponse updateArticle(1: i64 article_id, 2: i64 user_id, 3: ArticleUpdateRequest request) 
        throws (1: ArticleNotFoundException ex, 2: UnauthorizedException uex),
    
    // 删除文章
    bool deleteArticle(1: i64 article_id, 2: i64 user_id) 
        throws (1: ArticleNotFoundException ex, 2: UnauthorizedException uex),
    
    // 发布文章
    ArticleResponse publishArticle(1: i64 article_id, 2: i64 user_id) 
        throws (1: ArticleNotFoundException ex, 2: UnauthorizedException uex),
    
    // 增加浏览量
    void incrementViewCount(1: i64 article_id),
    
    // 点赞文章
    bool likeArticle(1: i64 article_id, 2: i64 user_id),
    
    // 添加评论
    Comment addComment(1: i64 user_id, 2: CommentCreateRequest request),
    
    // 获取文章评论
    list<Comment> getComments(1: i64 article_id),
}
