


namespace tensorflow {

  /// \brief 人脸属性类型定义
typedef enum {
  GENDER      = 0, ///< 性别, 0 = 不确定, 1 = 男性, 2 = 女性
  AGE         = 1, ///< 年龄
  POSE_PITCH  = 2, ///< 俯仰角
  POSE_YAW    = 3, ///< 偏航角
  POSE_ROLL   = 4, ///< 横滚角
  QUALITY     = 5, ///< 人脸质量
  LIVENESS_IR = 6, ///< 红外活体
  IMAGE_COLOR = 7, ///< 色彩
  FACE_MASK = 8,   ///< 口罩
} ArcternFaceAttrType ;
/// \brief 性别信息
typedef enum {
  MALE = 0,     ///< 男性
  FEMALE = 1,   ///< 女性
} ArcternFaceGenderType;
/// \brief 执行策略
enum class ExeMode : int {
  CUDA = 0, ///< cuda
  TRT = 1,  ///< tensorrt
  };

/// \brief 属性
/// sd

 enum ArcternFaceAttrType{
  GENDER      = 0, ///< 性别, 0 = 不确定, 1 = 男性, 2 = 女性
  AGE         = 1, ///< 年龄
  POSE_PITCH  = 2, ///< 俯仰角
  POSE_YAW    = 3, ///< 偏航角
  POSE_ROLL   = 4, ///< 横滚角
  QUALITY     = 5, ///< 人脸质量
  LIVENESS_IR = 6, ///< 红外活体
  IMAGE_COLOR = 7, ///< 色彩
  FACE_MASK = 8,   ///< 口罩
};


/// \brief  从授权服务平台获取授权文件.
/// \param  api_key - 授权平台生成的api_key
/// \param  api_secret - 授权平台生成的api_secret
/// \param  license_file - 授权文件存放地址，应该和config.json配置保持一致
/// \return  0 - Successed.
/// \return  非0值 - 失败，请基于错误码查找错误信息
ARCTERNSDK_API ARCTERN_INT arcternsdk_fetch_license(const char* api_key, const char* api_secret,
    const char* license_file);



/// \brief 回调函数，检测结束会调用此函数
/// \param result - 检测结果数组. result[0] 是RGB人脸检测结果,result[1]是IR人脸检测结果.
///                 如果没有人脸，则result[i].num等于0,result[i].rect等于NULL.
/// \param userdata - 用户自定义数据
typedef void (*ArcternSDK_AccessDetectCBF)(const ArcternDetectResult* result,
    void* userdata);


/// \brief  hisi图片信息，这个结构体仅仅为了加速海思平台的色彩空间转换
typedef struct {
  uint64_t vir_data[3];             ///< 图片虚拟地址指针
  uint64_t phy_data[3];             ///< 图片物理地址指针
  uint32_t stride[3];               ///< 步长
} ArcternHisiImgData;


class Graph;
class GraphDef;
class NodeBuilder;
struct CompositeOpScopes;


template<typename T> 
int add(T a, T b);

/// @addtogroup core
/// @{

/// A `Scope` object represents a set of related TensorFlow ops that have the
/// same properties such as a common name prefix.
///
/// A Scope object is a container for TensorFlow Op properties. Op constructors
/// get a Scope object as a mandatory first argument and the constructed op
/// acquires the properties in the object.
///
/// A simple example:
///
///     using namespace ops;
///     Scope root = Scope::NewRootScope();
///     auto c1 = Const(root, { {1, 1} });
///     auto m = MatMul(root, c1, { {41}, {1} });
///     GraphDef gdef;
///     Status s = root.ToGraphDef(&gdef);
///     if (!s.ok()) { ... }
///
/// Scope hierarchy:
///
/// The Scope class provides various With<> functions that create a new scope.
/// The new scope typically has one property changed while other properties are
/// inherited from the parent scope.
/// NewSubScope(name) method appends `name` to the prefix of names for ops
/// created within the scope, and WithOpName() changes the suffix which
/// otherwise defaults to the type of the op.
///
/// Name examples:
///
///     Scope root = Scope::NewRootScope();
///     Scope linear = root.NewSubScope("linear");
///     // W will be named "linear/W"
///     auto W = Variable(linear.WithOpName("W"),
///                       {2, 2}, DT_FLOAT);
///     // b will be named "linear/b_3"
///     int idx = 3;
///     auto b = Variable(linear.WithOpName("b_", idx),
///                       {2}, DT_FLOAT);
///     auto x = Const(linear, {...});  // name: "linear/Const"
///     auto m = MatMul(linear, x, W);  // name: "linear/MatMul"
///     auto r = BiasAdd(linear, m, b); // name: "linear/BiasAdd"
///
/// Scope lifetime:
///
/// A new scope is created by calling Scope::NewRootScope. This creates some
/// resources that are shared by all the child scopes that inherit from this
/// scope, directly or transitively. For instance, a new scope creates a new
/// Graph object to which operations are added when the new scope or its
/// children are used by an Op constructor. The new scope also has a Status
/// object which will be used to indicate errors by Op-constructor functions
/// called on any child scope. The Op-constructor functions have to check the
/// scope's status by calling the ok() method before proceeding to construct the
/// op.
///
/// Thread safety:
///
/// A `Scope` object is NOT thread-safe. Threads cannot concurrently call
/// op-constructor functions on the same `Scope` object.
class Scope {
  Scope(const Scope& other);
  ~Scope();
  Scope& operator=(const Scope& other);

  // The following functions are for users making graphs. They return brand new
  // scopes, or scopes derived from an existing scope object.

  /// Return a new scope.
  /// This creates a new graph and all operations constructed in this graph
  /// should use the returned object as the "root" scope.
  static Scope NewRootScope();

  /// Return a new scope. Ops created with this scope will have
  /// `name/child_scope_name` as the prefix. The actual name will be unique
  /// in the current scope. All other properties are inherited from the current
  /// scope. If `child_scope_name` is empty, the `/` is elided.
  Scope NewSubScope(const string& child_scope_name) const;

  /// Return a new scope. All ops created within the returned scope will have
  /// names of the form `name/StrCat(fragments...)[_suffix]`
  template <typename... Ty>
  Scope WithOpName(Ty... fragments) const {
    return WithOpNameImpl(absl::StrCat(fragments...));
  }

  /// Return a new scope. All ops created within the returned scope will have as
  /// control dependencies the union of operations in the control_deps vector
  /// and the control dependencies of the current scope.
  Scope WithControlDependencies(
      const gtl::ArraySlice<Operation>& control_deps) const;
  /// Same as above, but convenient to add control dependency on the operation
  /// producing the control_dep output.
  Scope WithControlDependencies(const Output& control_dep) const;

  /// Return a new scope. All ops created within the returned scope will have no
  /// control dependencies on other operations.
  Scope WithNoControlDependencies() const;

  /// Return a new scope. All ops created within the returned scope will have
  /// the device field set to 'device'.
  Scope WithDevice(const string& device) const;

  /// Returns a new scope.  All ops created within the returned scope will have
  /// their assigned device set to `assigned_device`.
  Scope WithAssignedDevice(const string& assigned_device) const;

  /// Returns a new scope.  All ops created within the returned scope will have
  /// their _XlaCluster attribute set to `xla_cluster`.
  Scope WithXlaCluster(const string& xla_cluster) const;

  /// Return a new scope. All ops created within the returned scope will be
  /// co-located on the device where op is placed.
  /// NOTE: This function is intended to be use internal libraries only for
  /// controlling placement of ops on to devices. Public use is not encouraged
  /// because the implementation of device placement is subject to change.
  Scope ColocateWith(const Operation& op) const;
  /// Convenience function for above.
  Scope ColocateWith(const Output& out) const { return ColocateWith(out.op()); }
  /// Clear all colocation constraints.
  Scope ClearColocation() const;

  /// Return a new scope. The op-constructor functions taking the returned scope
  /// as the scope argument will exit as soon as an error is detected, instead
  /// of setting the status on the scope.
  Scope ExitOnError() const;

  /// Return a new scope. All ops created with the new scope will have
  /// kernel_label as the value for their '_kernel' attribute;
  Scope WithKernelLabel(const string& kernel_label) const;

  // The following functions are for scope object consumers.

  /// Return a unique name, using default_name if an op name has not been
  /// specified.
  string GetUniqueNameForOp(const string& default_name) const;

  /// Update the status on this scope.
  /// Note: The status object is shared between all children of this scope.
  /// If the resulting status is not Status::OK() and exit_on_error_ is set on
  /// this scope, this function exits by calling LOG(FATAL).
  void UpdateStatus(const Status& s) const;

  // START_SKIP_DOXYGEN

  /// Update the builder with properties accumulated in this scope. Does not set
  /// status().
  // TODO(skyewm): NodeBuilder is not part of public API
  void UpdateBuilder(NodeBuilder* builder) const;
  // END_SKIP_DOXYGEN

  CompositeOpScopes GetCompositeOpScopes(const string& composite_op_name) const;

  bool ok() const;

  // TODO(skyewm): Graph is not part of public API
  Graph* graph() const;

  // TODO(skyewm): Graph is not part of public API
  std::shared_ptr<Graph> graph_as_shared_ptr() const;

  Status status() const;

  /// If status() is Status::OK(), convert the Graph object stored in this scope
  /// to a GraphDef proto and return Status::OK(). Otherwise, return the error
  /// status as is without performing GraphDef conversion.
  Status ToGraphDef(GraphDef* gdef) const;

  // START_SKIP_DOXYGEN

  /// If status() is Status::OK(), construct a Graph object using `opts` as the
  /// GraphConstructorOptions, and return Status::OK if graph construction was
  /// successful. Otherwise, return the error status.
  // TODO(josh11b, keveman): Make this faster; right now it converts
  // Graph->GraphDef->Graph.  This cleans up the graph (e.g. adds
  // edges from the source and to the sink node, resolves back edges
  // by name), and makes sure the resulting graph is valid.
  Status ToGraph(
      Graph* g, GraphConstructorOptions opts = GraphConstructorOptions{}) const;

  // Calls AddNode() using this scope's ShapeRefiner. This exists in the public
  // API to prevent custom op wrappers from needing access to shape_refiner.h or
  // scope_internal.h.
  // TODO(skyewm): remove this from public API
  Status DoShapeInference(Node* node) const;

  // Creates a new root scope that causes all DoShapeInference() calls to return
  // Status::OK() (on the returned scope and any subscopes). Used for testing.
  // TODO(skyewm): fix tests that still require this and eventually remove, or
  // at least remove from public API
  static Scope DisabledShapeInferenceScope();
  // END_SKIP_DOXYGEN

  const std::vector<Operation>& control_deps() const;

  // START_SKIP_DOXYGEN
  class Impl;
  Impl* impl() { return impl_.get(); }
  const Impl* impl() const { return impl_.get(); }
  // END_SKIP_DOXYGEN


  Scope WithOpNameImpl(const string& op_name) const;

  friend class InternalScope;
  std::unique_ptr<Impl> impl_;
  explicit Scope(Impl*);
};

/// A helper struct to hold the scopes that would be used by a function
/// constructing a composite op.
struct CompositeOpScopes {
  /// Scope to be used for creating the local ops (primitive or other composite
  /// ops).
  Scope child;
  /// Scope to be used for creating the last op.
  Scope last;
};

// Creates a node of the given operation, with the given inputs, and assigns the
// result to output. This does not support the ability to add additional
// attributes.
Status CreateOutputWithScope(string op_name,
                             absl::Span<const ::tensorflow::Input> inputs,
                             const Scope& scope, Output* output);
/// @}

}  // namespace tensorflow

#endif  // TENSORFLOW_CC_FRAMEWORK_SCOPE_H_

