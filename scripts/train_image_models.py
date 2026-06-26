import os
import time
import shutil
import gc
import tensorflow as tf

keras = tf.keras
layers = keras.layers
models = keras.models

ImageDataGenerator = keras.preprocessing.image.ImageDataGenerator
MobileNetV2 = keras.applications.MobileNetV2
EfficientNetB0 = keras.applications.EfficientNetB0
EarlyStopping = keras.callbacks.EarlyStopping

# =====================================================
# CONFIG
# =====================================================

DATASET_PATH = "datasets/images/final"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42

TEMP_DIR = "models/temp"

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs("models", exist_ok=True)

# =====================================================
# DATASET
# =====================================================

train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1
)

val_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2
)

train_data = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    seed=SEED
)

val_data = val_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    seed=SEED
)

NUM_CLASSES = train_data.num_classes

print("\nClass Mapping:")
print(train_data.class_indices)

results = {}

# =====================================================
# TRAIN FUNCTION
# =====================================================

def train_and_evaluate(model, model_name, save_path, epochs):

    print("\n" + "=" * 60)
    print(f"Training {model_name}")
    print("=" * 60)

    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True
    )

    start_time = time.time()

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    history = model.fit(
        train_data,
        validation_data=val_data,
        epochs=epochs,
        callbacks=[early_stop],
        verbose=1
    )

    training_time = time.time() - start_time

    val_acc = max(history.history["val_accuracy"])
    val_loss = min(history.history["val_loss"])

    model.save(save_path)

    results[model_name] = {
        "accuracy": val_acc,
        "loss": val_loss,
        "time": training_time,
        "path": save_path
    }

    print(f"\n{model_name} Saved")
    print(f"Validation Accuracy : {val_acc:.4f}")
    print(f"Validation Loss     : {val_loss:.4f}")

    tf.keras.backend.clear_session()
    gc.collect()

# =====================================================
# MODEL 1 : CNN
# =====================================================

cnn_model = models.Sequential([
    layers.Input(shape=(*IMG_SIZE, 3)),

    layers.Conv2D(32, (3, 3), activation="relu"),
    layers.MaxPooling2D(2, 2),

    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D(2, 2),

    layers.Conv2D(128, (3, 3), activation="relu"),
    layers.MaxPooling2D(2, 2),

    layers.Flatten(),

    layers.Dense(128, activation="relu"),
    layers.Dropout(0.5),

    layers.Dense(NUM_CLASSES, activation="softmax")
])

train_and_evaluate(
    cnn_model,
    "CNN",
    os.path.join(TEMP_DIR, "cnn_temp.keras"),
    epochs=10
)

# =====================================================
# MODEL 2 : MobileNetV2
# =====================================================

base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(*IMG_SIZE, 3)
)

base_model.trainable = False

mobilenet_model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(NUM_CLASSES, activation="softmax")
])

train_and_evaluate(
    mobilenet_model,
    "MobileNetV2",
    os.path.join(TEMP_DIR, "mobilenet_temp.keras"),
    epochs=5
)

# =====================================================
# MODEL 3 : EfficientNetB0
# =====================================================

base_model = EfficientNetB0(
    weights="imagenet",
    include_top=False,
    input_shape=(*IMG_SIZE, 3)
)

base_model.trainable = False

efficientnet_model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(NUM_CLASSES, activation="softmax")
])

train_and_evaluate(
    efficientnet_model,
    "EfficientNetB0",
    os.path.join(TEMP_DIR, "efficientnet_temp.keras"),
    epochs=5
)

# =====================================================
# COMPARISON
# =====================================================

print("\n")
print("=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

for model_name, data in results.items():
    print(
        f"{model_name:15} "
        f"Accuracy={data['accuracy']:.4f} "
        f"Loss={data['loss']:.4f} "
        f"Time={data['time']:.2f}s"
    )

best_model = max(
    results.items(),
    key=lambda x: x[1]["accuracy"]
)

best_name = best_model[0]
best_info = best_model[1]

print("\nBEST MODEL :", best_name)
print("BEST ACCURACY :", round(best_info["accuracy"] * 100, 2), "%")

# =====================================================
# SAVE FINAL MODEL
# =====================================================

shutil.copy(
    best_info["path"],
    "models/image_classifier.keras"
)

print("\nFinal model saved as:")
print("models/image_classifier.keras")

# =====================================================
# CLEANUP
# =====================================================

for file in os.listdir(TEMP_DIR):
    os.remove(os.path.join(TEMP_DIR, file))

print("\nTemporary files deleted.")
print("Training completed successfully.")